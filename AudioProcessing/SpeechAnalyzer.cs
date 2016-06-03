using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Numerics;
using Accord.Audio;
using Accord.Audio.Windows;
using Accord.Controls;
using Accord.Math;
using AForge.Math;
using Tools = Accord.Audio.Tools;

namespace AudioProcessing
{
    class SpeechAnalyzer : IDisposable
    {
        /// <summary>
        ///  Информация о сегменте речевого сигнала
        /// </summary>
        public struct SegmentInfo
        {
            /// <summary>
            /// Вокализирован сигнал или нет
            /// </summary>
            public bool IsVocalized;

            /// <summary>
            /// Частота основного тона
            /// </summary>
            public double FundamentalFrequency;

            /// <summary>
            /// Период основного тона
            /// </summary>
            public double FundamentalPeriod;

            /// <summary>
            /// Номер отсчета пика
            /// </summary>
            public int PeakIndex;

            /// <summary>
            /// Амплитуда пика вокализированного сигнала
            /// </summary>
            public double PeakPower;

            /// <summary>
            /// Высокочастотная энергия
            /// </summary>
            public double HighFrequencyEnergy;
            
            /// <summary>
            /// Мел-кепстральные коэффициенты
            /// </summary>
            public double[] MFCC;
        }


        // Количество сегментов, на которые разбивается сигнал
        public int SegmentsCount => _signal.Length/(_minStationaryVoiceSamples - _overlapSamples);
        public List<SegmentInfo> Segments => _segments;

        private readonly Signal _signal;
        private readonly int _nfft;
        private readonly int _minStationaryVoiceSamples;
        private readonly int _minFreqSample;
        private readonly int _maxFreqSample;
        private readonly int _minHFEnergyFreqSample;
        private readonly int _maxHFEnergyFreqSample;
        private readonly double _powerThreshold;
        private readonly int _overlapSamples;
        private readonly double[] _freqs;
        private readonly List<SegmentInfo> _segments;
        private readonly RaisedCosineWindow _window;

        private readonly int _melBankSize;
        private readonly double[,] _melBank;
        private readonly int _melTake;


        public SpeechAnalyzer(Signal signal)
        {
            _signal = signal;

            // Предполагаем что за 26.5мс голос статичен
            _minStationaryVoiceSamples = GetSamplesCountByTime(26.5);

            // Количество перекрывающих сэмплов (50% перекрытия)
            _overlapSamples = (int)(_minStationaryVoiceSamples * 0.5);

            // Граница амплитуды кепстра при которой сегмент считается вокализированным
            _powerThreshold = 0.1;

            // Количество отсчетов для преобразования Фурье, должно быть больше чем minVoicePartInSamples
            _nfft = 2048;

            // Минимальный индекс частоты основного тона, для 80Гц, для разной частоты дискретизации
            _minFreqSample = GetSampleIndexByFreq(80);

            // Максимальный индекс частоты основного тона, для 400Гц, для разной частоты дискретизации
            _maxFreqSample = GetSampleIndexByFreq(400);

            // Минимальный индекс начала высокочастотного участка (109Гц), для данного ДПФ
            _minHFEnergyFreqSample = GetSampleIndexByFreq(109);

            // Максимальный индекс начала высокочастотного участка (1012Гц), для данного ДПФ
            _maxHFEnergyFreqSample = GetSampleIndexByFreq(1012);

            // Вектор частот для данной частоты дискретизации
            _freqs = Accord.Audio.Tools.GetFrequencyVector(_nfft, _signal.SampleRate);

            // Окно Хэмминга для лучшей обработки краев сегмента
            _window = RaisedCosineWindow.Hamming(_minStationaryVoiceSamples);
            //_window = RaisedCosineWindow.Hann(_minStationaryVoiceSamples);
            //_window = RaisedCosineWindow.Rectangular(_minStationaryVoiceSamples);


            _melBankSize = 26;
            _melTake = 16;
            _melBank = new double[_melBankSize, _nfft / 2 + 1];

            BuildMelBank(300.0);

            _segments = new List<SegmentInfo>(SegmentsCount);
        }

        public void Compute()
        {
            var partData = new Complex[_nfft];

            // Цикл обхода по сегментам, startSample - номер первого отсчета сегмента
            for (var startSample = 0;
                startSample < _signal.Length - _minStationaryVoiceSamples;
                startSample += _minStationaryVoiceSamples - _overlapSamples)
            {
                // Применям окно, берем столько отсчтетов, сколько покрывает стационарность речевого сигнала,
                // От 10мс, до 40мс, количество заданно в _minStationaryVoiceSamples
                var part = _window.Apply(_signal, startSample);

                // Копируем в комплексную форму
                for (int i = 0; i < _minStationaryVoiceSamples; i++)
                    partData[i] = part.GetSample(0, i);

                // Оставшуюся часть заполняем нулями для ДПФ, т.к. ДПФ работает с количеством,
                // равным степеням двойки, поэтому добиваем до _nfft
                for (int i = _minStationaryVoiceSamples; i < _nfft; i++)
                    partData[i] = 0f;

                // Вычисляем информацию о сегменте
                var segment = ProceedSegment(partData);
                _segments.Add(segment);
            }
        }

        private SegmentInfo ProceedSegment(Complex[] segment)
        {
            //var cepstrum = Tools.GetPowerCepstrum((Complex[])segment.Clone());
            
            // Применяем ДПФ преобразование
            FourierTransform.FFT(segment, FourierTransform.Direction.Forward);

            // Посчитаем Мел-кепстральные коэффициенты
            var melCoeffs = GetMelCoeff(segment);

            // Вычислем кепстр, (мощность от частоты)
            var cepstrum = GetPowerCepstrumFromFFT(segment);

            // Найдем пик в заданном интервале
            var peakPower = 0.0;
            var peakIndex = 0;
            for (var i = _minFreqSample; i < _maxFreqSample; i++)
            {
                // Деление на nfft - это костыль (не нашел обоснования). Суть получается та же что и если делать через Tools.GetPowerCepstrum
                // но, ощутимо быстрее, т.к. не делаем лишний преобразований. В библиотечной функции - другой порядок дпф, сначала ifft, потом fft
                var power = Math.Abs(cepstrum[(int) i] / _nfft); 
                if (power > peakPower)
                {
                    peakIndex = (int)i;
                    peakPower = power;
                }
            }

            // Находим высокочастотную энергию
            // Получим АЧХ (Апмлитуда от частоты)
            var magnitude = Tools.GetMagnitudeSpectrum(segment);

            // Вычислим среднее значение высокочастотной энергии (в Дб)
            var volumeSum = 0.0;
            for (int i = _minHFEnergyFreqSample; i < _maxHFEnergyFreqSample; i++)
                volumeSum += GetVolumeFromMagnitude(magnitude[i]);

            var averageHfEnergy = volumeSum / (double)(_maxHFEnergyFreqSample - _minHFEnergyFreqSample);


            // Записываем результаты вычисление параметров сегмента
            var segmentInfo = new SegmentInfo()
            {
                // Сигнал вокализирован если амплитуда пика выше порога
                IsVocalized = peakPower > _powerThreshold,

                // Частота основного тона
                FundamentalFrequency = _freqs[peakIndex],

                // Период основного тона
                FundamentalPeriod = 1 / _freqs[peakIndex],

                // Амплитуда пика
                PeakPower = peakPower,

                // Индекс пика
                PeakIndex = peakIndex + _minFreqSample,

                // Высокочастотная энергия
                HighFrequencyEnergy = averageHfEnergy,

                // Мел-кепстральные коэффициенты
                MFCC = melCoeffs
            };

            return segmentInfo;
        }

        public double GetFrequencyMean()
        {
            return Accord.Statistics.Tools.Mean(
                _segments.Where(s => s.IsVocalized).Select(s => s.FundamentalFrequency).ToArray());
        }

        public double GetFrequencyStd()
        {
            return Accord.Statistics.Tools.StandardDeviation(
                _segments.Where(s => s.IsVocalized).Select(s => s.FundamentalFrequency).ToArray());
        }

        public double GetMeanHighFrequencyEnergy()
        {
            return Accord.Statistics.Tools.Mean(
               _segments.Where(s => s.IsVocalized).Select(s => s.HighFrequencyEnergy).ToArray());
        }

        public void GetRelativeJitterShimmer(out double jitter, out double shimmer)
        {
            var vocalized = _segments.Where(s => s.IsVocalized).ToArray();
            var n = (double)vocalized.Length; //Число вокализированных сегментов

            var periodDeltaSum = 0.0;
            var periodSum = 0.0;

            var powerDeltaSum = 0.0;
            var powerSum = 0.0;

            for (var i = 0; i < vocalized.Length; i++)
            {
                periodSum += vocalized[i].FundamentalPeriod;
                powerSum += vocalized[i].PeakPower;

                if (i >= 1)
                {
                    periodDeltaSum += Math.Abs(vocalized[i].FundamentalPeriod - vocalized[i-1].FundamentalPeriod);
                    powerDeltaSum += Math.Abs(vocalized[i].PeakPower - vocalized[i - 1].PeakPower);
                }
            }

            jitter = (periodDeltaSum / (n - 1)) / (periodSum / n);
            shimmer = (powerDeltaSum / (n - 1)) / (powerSum / n);
        }
        
        public int GetSampleIndexByFreq(double frequency)
        {
            return (int) Math.Ceiling(frequency/(_signal.SampleRate/(double) _nfft));
        }

        public int GetSamplesCountByTime(double time)
        {
            return (int)Math.Ceiling(time * _signal.SampleRate / 1000.0);
        }

        public static double GetVolumeFromMagnitude(double amplitude, double reference = 1.0)
        {
            return 20*Math.Log10(amplitude / reference);
        }

        public double[] GetMeanMFCC()
        {
            var sum = new double[_melTake];
            foreach (var segment in _segments)
            {
                for (int i = 0; i < _melTake; i++)
                {
                    if(segment.MFCC[i].IsReal())
                        sum[i] += segment.MFCC[i];
                }
            }

            for (int i = 0; i < _melTake; i++)
                sum[i] /= _segments.Count;

            return sum;
        }

        private static double[] GetPowerCepstrumFromFFT(Complex[] fft)
        {
            if (fft == null)
                throw new ArgumentNullException("signal");

            Complex[] logabs = new Complex[fft.Length];
            for (int i = 0; i < logabs.Length; i++)
                //logabs[i] = new Complex(System.Math.Log(fft[i].Magnitude), 0);
                logabs[i] = Math.Log(fft[i].Magnitude);

            FourierTransform.FFT(logabs, FourierTransform.Direction.Backward);
            return logabs.Re();
        }

        private static double ToMelScale(double frequency)
        {
            return 1125.0 * Math.Log(1 + frequency/700);
        }

        private static double FromMelScale(double melfrequency)
        {
            return 700 * (Math.Exp(melfrequency / 1125.0) - 1.0);
        }

        private double[] GetMelCoeff(Complex[] fft)
        {
            var powerSpectrum = Tools.GetPowerSpectrum(fft);
            var energies = new double[_melBankSize];
            

            for (var m = 0; m < _melBankSize; m++)
            {
                var power = 0.0;
                for (int sample = 1; sample < powerSpectrum.Length; sample++)
                {
                    power += _melBank[m, sample] * powerSpectrum[sample];
                }

                //energies[m] = Math.Log(power);
                energies[m] = power;
            }

            var coeff = new double[_melTake];

            // дискретное косинусное преобразование
            // первый элемент исключаем
            var N = (double)_melBankSize;
            for (var k = 0; k < _melTake; k++)
            {
                var sum = 0.0;
                var a = Math.Sqrt(2.0 / N);

                if(k == 0)
                    a = Math.Sqrt(1.0 / N);

                for (var n = 0; n < N; n++)
                {
                    sum += Math.Log(energies[n]) * Math.Cos(Math.PI * k * (n + 0.5) / N);
                }
                
                coeff[k] = a * sum;
            }


            //WavechartBox.Show(powerSpectrum.Select(v => (float)v).ToArray(), "PowerSpectrum", nonBlocking: true);
            //WavechartBox.Show(energies.Select(v => (float)v).ToArray(), "Mel energies", nonBlocking: true);
            //WavechartBox.Show(coeff.Skip(1).Select(v => (float)v).ToArray(), "Mel coeff");
            
            return coeff;
        }

        private void BuildMelBank(double minFrequency)
        {
            var minMel = ToMelScale(minFrequency);
            var maxMel = ToMelScale(_freqs[_nfft / 2]);

            for (int m = 0; m < _melBankSize; m++)
            {
                var leftFreq = minMel + (m / ((double)_melBankSize + 1)) * (maxMel - minMel);
                var centerFreq = minMel + ((m + 1) / ((double)_melBankSize + 1)) * (maxMel - minMel);
                var rightFreq = minMel + ((m + 2) / ((double)_melBankSize + 1)) * (maxMel - minMel);
                var left = FromMelScale(leftFreq);
                var center = FromMelScale(centerFreq);
                var right = FromMelScale(rightFreq);

                for (int sample = 0; sample < _nfft / 2 + 1; sample++)
                {
                    var k = _freqs[sample];

                    // bandpass filter
                    double h = 0.0;
                    if (k < left)
                        h = 0;
                    else if (k >= left && k <= center)
                        h = (k - left) / (center - left);
                    else if (k >= center && k <= right)
                        h = (right - k) / (right - center);
                    else if (k > right)
                        h = 0;

                    _melBank[m, sample] = h;
                }
            }
        }
        
        public void Dispose()
        {
            _signal?.Dispose();
        }
    }

    public static class Extensions
    {
        public static bool IsReal(this double value)
        {
            return !Double.IsNaN(value) && !Double.IsInfinity(value);
        }
    }
}
