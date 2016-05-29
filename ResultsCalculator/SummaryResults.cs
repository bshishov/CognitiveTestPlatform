namespace ResultsCalculator
{
    public class SummaryResults
    {
        public int Id;
        public string FolderName;
        public string Name;
        public int Age;

        public double ReactionAverage;
        public double ReactionMin;
        public double ReactionMax;
        public double ReactionFails;
        public double ReactionScore;

        public int TemperamentExtravertScore;
        public string TemperamentExtravertDescription;
        public int TemperamentNeurotismScore;
        public string TemperamentNeurotismDescription;
        public int TemperamentLieScore;
        public string TemperamentLieDescription;

        public int PlasticityTime;
        public double PlasticityAverageResponseTime;
        public int PlasticityFails;
        public double PlasticityScore;

        public int OperationTime;
        public double OperationAverageResponseTime;
        public int OperationFails;
        public double OperationScore;

        public int MemoryTime;
        public double MemoryAverageResponseTime;
        public int MemoryRemembered;
        public int MemoryScore;

        public double MemoryStressTime;
        public double MemoryStressAverageResponseTime;
        public double MemoryStressCorrectCount;
        public double MemoryStressWrongCount;
        public double MemoryStressScore;
    }
}