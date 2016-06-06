using System.IO;
using Accord.Audio;
using AudioProcessing;

namespace ResultsCalculator.Calculators
{
    class ReadingCalculator : ICalculator
    {
        public SummaryResults Compute(string resultsPath, SummaryResults summaryResults)
        {
            var path = ResultsCalculator.GetTestPathRawDirectory("reading", resultsPath);
            var audioPath = Path.Combine(path, "audio.wav");


            if (!File.Exists(audioPath))
                return summaryResults; // nothing to compute

            var speech = SpeechProcessing.ProcessWav(audioPath);

            summaryResults.ReadingF0Mean = speech.FundamentalFrequencyMean;
            summaryResults.ReadingF0Std = speech.FundamentalFrequencyStd;
            summaryResults.ReadingJitter = speech.Jitter;
            summaryResults.ReadingShimmer = speech.Shimmer;
            summaryResults.ReadingHFEnergy = speech.HighFrequencyEnergy;

            summaryResults.M1 = speech.MeanMFCC[0];
            summaryResults.M2 = speech.MeanMFCC[1];
            summaryResults.M3 = speech.MeanMFCC[2];
            summaryResults.M4 = speech.MeanMFCC[3];
            summaryResults.M5 = speech.MeanMFCC[4];
            summaryResults.M6 = speech.MeanMFCC[5];
            summaryResults.M7 = speech.MeanMFCC[6];
            summaryResults.M8 = speech.MeanMFCC[7];

            summaryResults.M9 = speech.MeanMFCC[8];
            summaryResults.M10 = speech.MeanMFCC[9];
            summaryResults.M11 = speech.MeanMFCC[10];
            summaryResults.M12 = speech.MeanMFCC[11];
            summaryResults.M13 = speech.MeanMFCC[12];
            summaryResults.M14 = speech.MeanMFCC[13];
            summaryResults.M15 = speech.MeanMFCC[14];
            summaryResults.M16 = speech.MeanMFCC[15];

            return summaryResults;
        }
    }
}
