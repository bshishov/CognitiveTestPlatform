namespace ResultsCalculator
{
    interface ICalculator
    {
        SummaryResults Compute(string resultsPath, SummaryResults summaryResults);
    }
}