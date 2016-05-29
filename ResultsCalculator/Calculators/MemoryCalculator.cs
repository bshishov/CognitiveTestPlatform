using System.Collections;
using System.IO;
using System.Linq;
using Newtonsoft.Json;
using Shared;

namespace ResultsCalculator.Calculators
{
    class MemoryCalculator : ICalculator
    {
        public SummaryResults Compute(string resultsPath, SummaryResults summaryResults)
        {
            var path = ResultsCalculator.GetTestPathRawDirectory("memory", resultsPath);
            var eventsRaw = JsonConvert.DeserializeObject(File.ReadAllText(Path.Combine(path, "events.json")));

            var events = ((IEnumerable)eventsRaw).Cast<dynamic>().ToList();
            var remembered = events.Count(e => e.name == "success");
            var averageCorrectTime = events.Where(e => e.name == "success").Average(e => e.args.reaction);
            var endTime = (int?)events.FirstOrDefault(e => e.name == "test_complete")?.time;
            var score = events.Where(e => e.name == "success").Sum(e =>
            {
                if (e.args.reaction < 4000)
                    return 5;
                if (e.args.reaction < 8000)
                    return 4;
                return 3;
            });

            summaryResults.MemoryRemembered = remembered;
            summaryResults.MemoryScore = score;
            summaryResults.MemoryTime = endTime.GetValueOrDefault();
            summaryResults.MemoryAverageResponseTime = averageCorrectTime;


            var detailedResults = ResultsCalculator.GetTestDirectory("memory", resultsPath);
            using (var csv = new CsvWriter(Path.Combine(detailedResults, "timeline.csv"), "time", "reaction", "remembered", "fails"))
            {
                var fails = 0;

                foreach (var e in events)
                {
                    if (e.name == "fail")
                        fails++;

                    if (e.name == "success" || e.name == "fail")
                        csv.Write((int)e.time, (int)e.args.reaction, (int)e.args.remembered, fails);
                }
            }


            return summaryResults;
        }
    }
}