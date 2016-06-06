using System.Collections;
using System.IO;
using System.Linq;
using Newtonsoft.Json;

namespace ResultsCalculator.Calculators
{
    class TemperamentCalculator : ICalculator
    {

        // Test keys
        private readonly int[] _extravertYes = {1, 3, 8, 10, 13, 17, 22, 25, 27, 39, 44, 46, 49, 53, 56};
        private readonly int[] _extravertNo = { 5, 15, 20, 29, 32, 34, 37, 41, 51 };

        private readonly int[] _neurotismYes = { 2, 4, 7, 9, 11, 14, 16, 19, 21, 23, 26, 28, 31, 33, 35, 38, 40, 43, 45, 47, 50, 52, 55, 57 };

        private readonly int[] _lieYes = { 6, 24, 36 };
        private readonly int[] _lieNo = { 12, 18, 30, 42, 48, 54 };


        public SummaryResults Compute(string resultsPath, SummaryResults summaryResults)
        {
            var path = ResultsCalculator.GetTestPathRawDirectory("temperament", resultsPath);
            var eventsRaw = JsonConvert.DeserializeObject(File.ReadAllText(Path.Combine(path, "events.json")));

            var events = ((IEnumerable)eventsRaw).Cast<dynamic>();

            var answers = events.Where(e => e.name == "answer").Select(e => e.args);

            var extravertScore = 0;
            var neurotismScore = 0;
            var lieScore = 0;

            foreach (var answer in answers)
            {
                var choice = answer.answer; // "yes" or "no"
                var id = (int) answer.question.id;

                if (choice == "yes")
                {
                    if (_extravertYes.Contains(id))
                        extravertScore++;

                    if (_neurotismYes.Contains(id))
                        neurotismScore++;

                    if (_lieYes.Contains(id))
                        lieScore++;
                }

                if (choice == "no")
                {
                    if (_extravertNo.Contains(id))
                        extravertScore++;

                    if (_lieNo.Contains(id))
                        lieScore++;
                }
            }

            if (extravertScore > 15)
                summaryResults.TemperamentExtravertDescription = "Яркий экстраверт";
            else if (extravertScore > 12)
                summaryResults.TemperamentExtravertDescription = "Склонность к экстраверсии";
            else if (extravertScore == 12)
                summaryResults.TemperamentExtravertDescription = "Среднее значение экстраверсии";
            else if (extravertScore > 9)
                summaryResults.TemperamentExtravertDescription = "Склонность к интроверсии";
            else if (extravertScore > 5)
                summaryResults.TemperamentExtravertDescription = "Интроверт";
            else
                summaryResults.TemperamentExtravertDescription = "Глубокий интроверт";

            if (neurotismScore > 19)
                summaryResults.TemperamentNeurotismDescription = "Очень высокий уровень нейротизма";
            else if (extravertScore > 13)
                summaryResults.TemperamentNeurotismDescription = "Высокий уровень нейротизма";
            else if (extravertScore > 9)
                summaryResults.TemperamentNeurotismDescription = "Среднее значение нейротизма";
            else
                summaryResults.TemperamentNeurotismDescription = "Низкий уровень нейротизма";

            if (lieScore > 4)
                summaryResults.TemperamentLieDescription = "Неискренность в ответах";
            else
                summaryResults.TemperamentLieDescription = "Норма";

            summaryResults.TemperamentExtravertScore = extravertScore;
            summaryResults.TemperamentNeurotismScore = neurotismScore;
            summaryResults.TemperamentLieScore = lieScore;
            return summaryResults;
        }
    }
}