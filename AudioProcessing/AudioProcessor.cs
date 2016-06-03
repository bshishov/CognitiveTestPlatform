using System.IO;
using Accord.Audio;
using Shared;

namespace AudioProcessing
{
    public class SpeechInfo
    {
        public double FundamentalFrequencyMean;
        public double FundamentalFrequencyStd;
        public double Jitter;
        public double Shimmer;
        public double HighFrequencyEnergy;
        public double[] MeanMFCC;
    }

    public static class SpeechProcessing
    {
        public static SpeechInfo ProcessWav(string wavPath, string saveTo="")
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
                    HighFrequencyEnergy = speech.GetMeanHighFrequencyEnergy(),
                    MeanMFCC = speech.GetMeanMFCC()
                };
                speech.GetRelativeJitterShimmer(out info.Jitter, out info.Shimmer);

                if (!string.IsNullOrEmpty(saveTo))
                {
                    using (var csv = new CsvWriter(saveTo, "IsVocalized", "F0", "T0", "HFEnergy", "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10", "M11", "M12", "M13", "M14", "M15", "M16"))
                    {
                        foreach (var segment in speech.Segments)
                        {
                            csv.Write(segment.IsVocalized, segment.FundamentalFrequency, segment.FundamentalPeriod, segment.HighFrequencyEnergy,
                                segment.MFCC[0], segment.MFCC[1], segment.MFCC[2], segment.MFCC[3], segment.MFCC[4], segment.MFCC[5], segment.MFCC[6], segment.MFCC[7], segment.MFCC[8],
                                segment.MFCC[9], segment.MFCC[10], segment.MFCC[11], segment.MFCC[12], segment.MFCC[13], segment.MFCC[14], segment.MFCC[15]);
                        }
                    }
                }
                return info;
            }
        }
    }
}

