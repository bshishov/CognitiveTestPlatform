using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Numerics;
using Accord.Audio;
using Accord.Audio.Windows;
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
            public bool IsVocalized;
            public double FundamentalFrequency;
            public double FundamentalPeriod;
            public int PeakIndex;
            public double PeakPower;
            public double HighFrequencyEnergy;
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
                HighFrequencyEnergy = averageHfEnergy
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

        public void Dispose()
        {
            _signal?.Dispose();
        }
    }
}
