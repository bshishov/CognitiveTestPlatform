using System.Collections;
using System.IO;
using System.Linq;
using Newtonsoft.Json;
using Shared;

namespace ResultsCalculator.Calculators
{
    class ReactionCalculator : ICalculator
    {
        public SummaryResults Compute(string resultsPath, SummaryResults summaryResults)
        {
            var path = ResultsCalculator.GetTestPathRawDirectory("reaction", resultsPath);
            var eventsRaw = JsonConvert.DeserializeObject(File.ReadAllText(Path.Combine(path, "events.json")));

            var events = ((IEnumerable) eventsRaw).Cast<dynamic>();

            var successEvents = events.Where(e => e.name == "success").ToList();

            var averageReaction = successEvents.Average(e => e.args.reaction);
            var minReaction = successEvents.Min(e => e.args.reaction);
            var maxReaction = successEvents.Max(e => e.args.reaction);
            var fails = events.Count(e => e.name == "fail");

            var score = 0.0;
            if (averageReaction <= 250)
                score = 100;
            else if(averageReaction > 250 && averageReaction < 350)
                score = 100 - (averageReaction - 250);
            else
                score = 0;

            summaryResults.ReactionAverage = averageReaction;
            summaryResults.ReactionMin = minReaction;
            summaryResults.ReactionMax = maxReaction;
            summaryResults.ReactionScore = score;
            summaryResults.ReactionFails = fails;


            var detailedResults = ResultsCalculator.GetTestDirectory("reaction", resultsPath);
            using (var csv = new CsvWriter(Path.Combine(detailedResults, "timeline.csv"), "time", "reaction", "correct", "wrong"))
            {
                var correct = 0;
                var wrong = 0;

                foreach (var e in events)
                {
                    if (e.name == "success")
                        correct++;

                    if (e.name == "fail")
                        wrong++;

                    if (e.name == "success")
                        csv.Write((int)e.time, (int)e.args.reaction, correct, wrong);

                    if (e.name == "fail")
                        csv.Write((int)e.time, null, correct, wrong);
                }
            }


            return summaryResults;
        }
    }
}