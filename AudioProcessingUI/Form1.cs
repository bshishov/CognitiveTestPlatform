using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Numerics;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Accord.Audio;
using Accord.Audio.Generators;
using Accord.Audio.Windows;
using Accord.Controls;
using Accord.Math;
using Accord.Statistics;
using Accord.Statistics.Testing;
using AForge;
using AForge.Controls;
using AForge.Math;
using AudioProcessing;

namespace AudioProcessingUI
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            var dir = new DirectoryInfo("C:\\tests\\db2");
            var files = dir.EnumerateFiles("*.wav", SearchOption.AllDirectories);
            
            foreach (var file in files)
            {
                Analyze(file.FullName);
            }
            
            /*
            {
                Analyze("C:\\tests\\welcome_back.wav", out fomean, out fostd, out jitter, out shimmer);
                Analyze("C:\\tests\\colors.wav", out fomean, out fostd, out jitter, out shimmer);
                Analyze("C:\\tests\\audio1.wav", out fomean, out fostd, out jitter, out shimmer);
                Analyze("C:\\tests\\audio2.wav", out fomean, out fostd, out jitter, out shimmer);
                Analyze("C:\\tests\\audio3.wav", out fomean, out fostd, out jitter, out shimmer);
                Analyze("C:\\tests\\audio4.wav", out fomean, out fostd, out jitter, out shimmer);
            }*/
        }

        private void Analyze(string path)
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
            WavechartBox.Show(speech.Segments.Select(s => s.IsVocalized ? (float)s.FundamentalFrequency : float.NaN).ToArray(), "F0");

            var mean = speech.GetFrequencyMean();
            var std = speech.GetFrequencyStd();
            double jitter, shimmer;
            speech.GetRelativeJitterShimmer(out jitter, out shimmer);

            Debug.WriteLine($"Analyzing {path}: Fomean={mean:F}, Fostd={std:F}, Jitter={jitter:F}, Shimmer={shimmer:F}");
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
    }
}
