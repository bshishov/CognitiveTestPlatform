using System;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Windows.Forms;
using Accord.Audio;
using AForge.Controls;
using AudioProcessing;
using Shared;

namespace AudioProcessingUI
{
    public partial class MainForm : Form
    {
        public MainForm()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            //var dir = new DirectoryInfo("D:\\SpeechDB\\Liberman M Emotional Prosody Speech and Transcripts");


            
        }

        private SpeechResult Analyze(string path)
        {
            Signal rawsignal;
            using (var reader = new WaveReader())
            {
                reader.Open(File.OpenRead(path));
                rawsignal = reader.Decode();
            }

            var speech = new SpeechAnalyzer(rawsignal);
            speech.Compute();
            //WavechartBox.Show(speech.Segments.Select(s => s.IsVocalized ? (float)s.FundamentalFrequency : float.NaN).ToArray(), "F0", nonBlocking: true);
            //WavechartBox.Show(speech.Segments.Select(s => (float)s.PeakPower).ToArray(), "PeakPower", nonBlocking: true);
            //WavechartBox.Show(speech.Segments.Select(s => (float)s.FundamentalFrequency).ToArray(), "FundamentalFrequency", nonBlocking: true);
            //WavechartBox.Show(speech.Segments.Select(s => s.IsVocalized ? (float)s.FundamentalFrequency : float.NaN).ToArray(), "FundamentalFrequency");
            //WavechartBox.Show(speech.Segments.Select(s => s.IsVocalized ? (float)s.FundamentalPeriod : float.NaN).ToArray(), "FundamentalPeriod");
            //WavechartBox.Show(speech.Segments.Select(s => s.IsVocalized ? (float)s.HighFrequencyEnergy : float.NaN).ToArray(), "HighFrequencyEnergy");

            var mean = speech.GetFrequencyMean();
            var std = speech.GetFrequencyStd();
            var hfEnergy = speech.GetMeanHighFrequencyEnergy();
            double jitter, shimmer;
            speech.GetRelativeJitterShimmer(out jitter, out shimmer);


            var classIndex = -1;
            var className = "";
            if (path.Contains("нейтраль"))
            {
                classIndex = 0;
                className = "нейтраль";
            }

            if (path.Contains("гнев"))
            {
                classIndex = 1;
                className = "гнев";
            }

            if (path.Contains("печаль"))
            {
                classIndex = 2;
                className = "печаль";
            }

            if (path.Contains("радость"))
            {
                classIndex = 3;
                className = "радость";
            }
            if (path.Contains("страх"))
            {
                classIndex = 4;
                className = "страх";
            }

            var result = new SpeechResult()
            {
                F0Mean = mean,
                F0Std = std,
                Jitter = jitter,
                Shimmer = shimmer,
                HFEnergy = hfEnergy
            };
            
            Debug.WriteLine($"Analyzing {path}: Fomean={mean:F}, Fostd={std:F}, Jitter={jitter:F}, Shimmer={shimmer:F}, hfEnergy={hfEnergy:F}");
            return result;
        }

        private void ShowChart(double[] source, string name)
        {
            var data = new double[source.Length, 2];
            for (int i = 0; i < source.Length; i++)
            {
                data[i, 0] = i;
                data[i, 1] = source[i];
            }

            var chart = new Chart() { Dock = DockStyle.Fill, BackColor = Color.White };
            chart.RangeX = new AForge.Range(0, source.Length);
            chart.AddDataSeries(name, Color.Blue, Chart.SeriesType.Dots, 5);
            chart.UpdateDataSeries(name, data);

            using (var form = new Form() {Text = name})
            {
                form.Controls.Add(chart);
                form.ShowDialog();
            }
        }

        private void TestResultsButton_Click(object sender, EventArgs e)
        {
            using (var plasticity = new CsvWriter("D:\\TestResultsFromWeb\\plasticity.csv", "Path", "F0Mean", "F0Std", "Jitter", "Shimmer", "HFEnergy"))
            using (var reading = new CsvWriter("D:\\TestResultsFromWeb\\reading.csv", "Path", "F0Mean", "F0Std", "Jitter", "Shimmer", "HFEnergy"))
            {
                var dir = new DirectoryInfo("D:\\TestResultsFromWeb");
                var files = dir.EnumerateFiles("*.wav", SearchOption.AllDirectories);

                foreach (var file in files)
                {
                    var result = Analyze(file.FullName);

                    CsvWriter writer = null;
                    if (file.FullName.Contains("plasticity"))
                        writer = plasticity;

                    if (file.FullName.Contains("reading"))
                        writer = reading;

                    writer?.Write(file.FullName, result.F0Mean, result.F0Std, result.Jitter, result.Shimmer, result.HFEnergy);
                }
            }
        }

        /*
        private void InitializeComponent()
        {
            this.SuspendLayout();
            // 
            // MainForm
            // 
            this.ClientSize = new System.Drawing.Size(585, 410);
            this.Name = "MainForm";
            this.ResumeLayout(false);

        }*/
    }
}