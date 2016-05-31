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

            return summaryResults;
        }
    }
}
