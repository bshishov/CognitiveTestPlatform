using System.IO;
using Accord.Audio;

namespace AudioProcessing
{
    public class SpeechInfo
    {
        public double FundamentalFrequencyMean;
        public double FundamentalFrequencyStd;
        public double Jitter;
        public double Shimmer;
        public double HighFrequencyEnergy;
    }

    public static class SpeechProcessing
    {
        public static SpeechInfo ProcessWav(string wavPath)
        {
            Signal signal = null;

            using (var stream = File.OpenRead(wavPath))
            using (var reader = new WaveReader())
            {
                reader.Open(stream);
                signal = reader.Decode();
            }

            using (var speech = new SpeechAnalyzer(signal))
            {
                speech.Compute();
                var info = new SpeechInfo
                {
                    FundamentalFrequencyMean = speech.GetFrequencyMean(),
                    FundamentalFrequencyStd = speech.GetFrequencyStd(),
                    HighFrequencyEnergy = speech.GetMeanHighFrequencyEnergy()
                };
                speech.GetRelativeJitterShimmer(out info.Jitter, out info.Shimmer);

                return info;
            }
        }
    }
}

