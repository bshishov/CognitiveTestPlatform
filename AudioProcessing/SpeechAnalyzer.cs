using System;
using System.Collections.Generic;
using System.Linq;
using System.Numerics;
using Accord.Audio;
using Accord.Audio.Windows;

namespace AudioProcessing
{
    public class SpeechAnalyzer
    {
        public struct SegmentInfo
        {
            public bool IsVocalized;
            public double FundamentalFrequency;
            public double FundamentalPeriod;
            public int PeakIndex;
            public double PeakPower;
        }


        // Количество сегментов, на которые разбивается сигнал
        public int SegmentsCount => _signal.Length/(_minStationaryVoiceSamples - _overlapSamples);
        public List<SegmentInfo> Segments => _segments;

        private readonly Signal _signal;
        private readonly int _nfft;
        private readonly int _minStationaryVoiceSamples;
        private readonly int _minFreqSample;
        private readonly int _maxFreqSample;
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

            // Количество перекрывающих сэмплов (20% перекрытия)
            _overlapSamples = (int)(_minStationaryVoiceSamples * 0.2);

            // Граница амплитуды кепстра при которой сегмент считается вокализированным
            _powerThreshold = 0.1;

            // Количество отсчетов для преобразования Фурье, должно быть больше чем minVoicePartInSamples
            _nfft = 2048;

            // Минимальный индекс частоты основного тона, для 80Гц, для разной частоты дискретизации
            _minFreqSample = GetSampleIndexByFreq(80);

            // Максимальный индекс частоты основного тона, для 400Гц, для разной частоты дискретизации
            _maxFreqSample = GetSampleIndexByFreq(400);

            // Вектор частот для данной частоты дискретизации
            _freqs = Accord.Audio.Tools.GetFrequencyVector(_nfft, _signal.SampleRate);

            // Окно Хэмминга для лучшей обработки краев сегмента
            _window = RaisedCosineWindow.Hamming(_minStationaryVoiceSamples);
            //var window = RaisedCosineWindow.Hann(minStationaryVoiceSamples);
            //var window = RaisedCosineWindow.Rectangular(minStationaryVoiceSamples);


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

        private SegmentInfo ProceedSegment(Complex[] segment)
        {
            // Вычислем кепстр
            var cepstrum = Tools.GetPowerCepstrum(segment);

            // Найдем пик в заданном интервале
            var peakPower = -100.0;
            var peakIndex = 0;
            for (var i = _minFreqSample; i < _maxFreqSample; i++)
            {
                if (cepstrum[(int)i] > peakPower)
                {
                    peakIndex = (int)i;
                    peakPower = cepstrum[(int)i];
                }
            }

            // Записываем результаты вычисление параметров сегмента
            var segmentInfo = new SegmentInfo()
            {
                // Сигнал вокализирован если амплитуда пика выше порога
                IsVocalized = peakPower > _powerThreshold,

                // Частота основного тона
                FundamentalFrequency = _freqs[peakIndex],

                // Период основного тона
                FundamentalPeriod = 1/_freqs[peakIndex],

                // Амплитуда пика
                PeakPower = peakPower,

                PeakIndex = peakIndex + _minFreqSample
            };

            return segmentInfo;
        }

        public int GetSampleIndexByFreq(double frequency)
        {
            return (int) Math.Ceiling(frequency/(_signal.SampleRate/(double) _nfft));
        }

        public int GetSamplesCountByTime(double time)
        {
            return (int)Math.Ceiling(time * _signal.SampleRate / 1000.0);
        }
    }
}
