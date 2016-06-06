using System.Collections;
using System.IO;
using System.Linq;
using Newtonsoft.Json;
using Shared;

namespace ResultsCalculator.Calculators
{
    class MemoryStressCalculator : ICalculator
    {
        public SummaryResults Compute(string resultsPath, SummaryResults summaryResults)
        {
            var path = ResultsCalculator.GetTestPathRawDirectory("memorystress", resultsPath);
            var eventsRaw = JsonConvert.DeserializeObject(File.ReadAllText(Path.Combine(path, "events.json")));

            var events = ((IEnumerable)eventsRaw).Cast<dynamic>().ToList();

            var endTime = (int?)events.FirstOrDefault(e => e.name == "test_complete")?.time;
            var correctCount = events.Count(e => e.name == "correct");
            var wrongCount = events.Count(e => e.name == "wrong");
            var averageResponseTime =
                events.Where(e => e.name == "wrong" || e.name == "correct").Average(e => e.args.decisionTime);

            var score = correctCount * 3 + (correctCount - wrongCount) * 2 + (6 - (int)(averageResponseTime / 1000.0)) * 2;

            summaryResults.MemoryStressTime = endTime.GetValueOrDefault();
            summaryResults.MemoryStressCorrectCount = correctCount;
            summaryResults.MemoryStressWrongCount = wrongCount;
            summaryResults.MemoryStressAverageResponseTime = averageResponseTime;
            summaryResults.MemoryStressScore = score;


            var detailedResults = ResultsCalculator.GetTestDirectory("memorystress", resultsPath);
            using (var csv = new CsvWriter(Path.Combine(detailedResults, "timeline.csv"), "time", "decisionTime", "correct", "wrong"))
            {
                var correct = 0;
                var wrong = 0;

                foreach (var e in events)
                {
                    if (e.name == "correct")
                        correct++;

                    if (e.name == "wrong")
                        wrong++;

                    if(e.name == "correct" || e.name == "wrong")
                        csv.Write((int)e.time, (int)e.args.decisionTime, correct, wrong);
                }
            }

            return summaryResults;
        }
    }
}