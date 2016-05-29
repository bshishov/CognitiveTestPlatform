using System.Collections;
using System.IO;
using System.Linq;
using Newtonsoft.Json;
using Shared;

namespace ResultsCalculator.Calculators
{
    class PlasticityCalculator : ICalculator
    {
        public SummaryResults Compute(string resultsPath, SummaryResults summaryResults)
        {

            var path = ResultsCalculator.GetTestPathRawDirectory("plasticity", resultsPath);
            var eventsRaw = JsonConvert.DeserializeObject(File.ReadAllText(Path.Combine(path, "events.json")));

            var events = ((IEnumerable)eventsRaw).Cast<dynamic>().ToList();

            var averageCorrectTime = events.Where(e => e.name == "correct").Average(e => e.args.reaction);
            var wrongCount = events.Count(e => e.name == "wrong");
            var endTime = (int?)events.FirstOrDefault(e => e.name == "test_complete")?.time;
            var score = 100.0;

            if (endTime > 40000)
            {
                score -= 2*(endTime.GetValueOrDefault() - 40000)/1000.0;
            }

            score -= wrongCount*10;

            summaryResults.PlasticityAverageResponseTime = averageCorrectTime;
            summaryResults.PlasticityFails = wrongCount;
            summaryResults.PlasticityTime = endTime.GetValueOrDefault();
            summaryResults.PlasticityScore = score;

            var detailedResults = ResultsCalculator.GetTestDirectory("plasticity", resultsPath);
            using (var csv = new CsvWriter(Path.Combine(detailedResults, "timeline.csv"), "time", "reaction", "currenttext", "currentcolor", "selected", "correct", "wrong"))
            {
                var correct = 0;
                var wrong = 0;

                foreach (var e in events)
                {
                    if (e.name == "correct")
                        correct++;

                    if (e.name == "wrong")
                        wrong++;

                    if (e.name == "correct" || e.name == "wrong")
                        csv.Write((int)e.time, (int)e.args.reaction, e.args.current.text, e.args.current.colorName, e.args.selected, correct, wrong);
                }
            }


            return summaryResults;
        }
    }
}