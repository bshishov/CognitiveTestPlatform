using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using ResultsCalculator.Calculators;

namespace ResultsCalculator
{
    public class ResultsCalculator
    {
        private readonly string _rootPath;
        private readonly ICalculator[] _calculators;

        public ResultsCalculator(string path)
        {
            _rootPath = path;
            _calculators = new ICalculator[]
            {
                new ReadingCalculator(),
                new TemperamentCalculator(), 
                new ReactionCalculator(),
                new PlasticityCalculator(), 
                new OperationCalculator(), 
                new MemoryCalculator(),
                new MemoryStressCalculator(), 
            };
        }

        public SummaryResults Compute(SummaryResults res)
        {
            foreach (var calculator in _calculators)
            {
                try
                {
                    res = calculator.Compute(_rootPath, res);
                }
                catch (Exception ex)
                {
                    Debug.WriteLine(ex.Message);
                }
            }
            
            return res;
        }

        public static string GetTestDirectory(string testName, string resultsPath)
        {
            var dir = new DirectoryInfo(resultsPath);
            var testDirectories = dir.GetDirectories(testName + "*", SearchOption.TopDirectoryOnly);
            return testDirectories.Last().FullName;
        }

        public static string GetTestPathRawDirectory(string testName, string resultsPath)
        {
            return Path.Combine(GetTestDirectory(testName, resultsPath), "raw");
        }
    }
}
