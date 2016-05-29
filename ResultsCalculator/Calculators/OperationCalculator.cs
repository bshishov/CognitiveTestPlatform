using System.Collections;
using System.IO;
using System.Linq;
using Newtonsoft.Json;
using Shared;

namespace ResultsCalculator.Calculators
{
    class OperationCalculator : ICalculator
    {
        public SummaryResults Compute(string resultsPath, SummaryResults summaryResults)
        {
            var path = ResultsCalculator.GetTestPathRawDirectory("operation", resultsPath);
            var eventsRaw = JsonConvert.DeserializeObject(File.ReadAllText(Path.Combine(path, "events.json")));

            var events = ((IEnumerable)eventsRaw).Cast<dynamic>().ToList();

            var averageCorrectTime = events.Where(e => e.name == "correct").Average(e => e.args.reaction);
            var wrongCount = events.Count(e => e.name == "wrong");
            var endTime = (int?)events.FirstOrDefault(e => e.name == "test_complete")?.time;

            var score = 100.0;
            if (endTime > 65000)
            {
                score -= 1 * (endTime.GetValueOrDefault() - 65000) / 1000.0;
            }

            score -= wrongCount * 10;

            summaryResults.OperationAverageResponseTime = averageCorrectTime;
            summaryResults.OperationFails = wrongCount;
            summaryResults.OperationTime = endTime.GetValueOrDefault();
            summaryResults.OperationScore = score;


            var detailedResults = ResultsCalculator.GetTestDirectory("operation", resultsPath);
            using (var csv = new CsvWriter(Path.Combine(detailedResults, "timeline.csv"), "time", "left", "right", "choice", "reaction", "correct", "wrong"))
            {
                var correct = 0;
                var wrong = 0;
                var left = "";
                var right = "";

                foreach (var e in events)
                {
                    if (e.name == "start")
                    {
                        left = e.args.left;
                        right = e.args.right;
                    }

                    if (e.name == "correct")
                    {
                        correct++;
                    }

                    if (e.name == "wrong")
                    {
                        wrong++;
                    }
                    

                    if (e.name == "correct" || e.name == "wrong")
                        csv.Write((int)e.time, left, right, e.args.choice, (int)e.args.reaction, correct, wrong);
                }
            }

            return summaryResults;
        }
    }
}