namespace ResultsCalculator
{
    public class SummaryResults
    {
        public int Id;
        public string FolderName;
        public string Name;
        public int Age;

        public double ReadingF0Mean;
        public double ReadingF0Std;
        public double ReadingJitter;
        public double ReadingShimmer;
        public double ReadingHFEnergy;

        public double M1;
        public double M2;
        public double M3;
        public double M4;
        public double M5;
        public double M6;
        public double M7;
        public double M8;
        public double M9;
        public double M10;
        public double M11;
        public double M12;
        public double M13;
        public double M14;
        public double M15;
        public double M16;

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