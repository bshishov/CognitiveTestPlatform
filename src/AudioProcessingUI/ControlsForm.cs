using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using AudioProcessing;
using Shared;

namespace AudioProcessingUI
{
    public partial class ControlsForm : Form
    {
        public ControlsForm()
        {
            InitializeComponent();
            sourcePathTextbox.Text = "D:\\results\\";
            destPathTextbox.Text = "D:\\results\\audio.csv";
        }

        private void button2_Click(object sender, EventArgs e)
        {
            using (var writer = new CsvWriter(destPathTextbox.Text, "Path", "F0Mean", "F0Std", "Jitter", "Shimmer", "HFEnergy", 
                "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10", "M11", "M12", "M13", "M14", "M15", "M16"))
            {
                var dir = new DirectoryInfo(sourcePathTextbox.Text);
                var files = dir.EnumerateFiles("*.wav", SearchOption.AllDirectories);

                foreach (var file in files)
                {
                    if (!string.IsNullOrEmpty(containsTextbox.Text) && !file.FullName.Contains(containsTextbox.Text))
                        continue;

                    var parentDir = Path.GetDirectoryName(Path.GetDirectoryName(file.FullName));
                    var speech = SpeechProcessing.ProcessWav(file.FullName, Path.Combine(parentDir, file.Name + ".csv"));
                    writer.Write(file.FullName, 
                        speech.FundamentalFrequencyMean,
                        speech.FundamentalFrequencyStd, 
                        speech.Jitter, 
                        speech.Shimmer, 
                        speech.HighFrequencyEnergy,
                        speech.MeanMFCC[0], speech.MeanMFCC[1], speech.MeanMFCC[2], speech.MeanMFCC[3], speech.MeanMFCC[4], speech.MeanMFCC[5], speech.MeanMFCC[6], speech.MeanMFCC[7], speech.MeanMFCC[8],
                        speech.MeanMFCC[9], speech.MeanMFCC[10], speech.MeanMFCC[11], speech.MeanMFCC[12], speech.MeanMFCC[13], speech.MeanMFCC[14], speech.MeanMFCC[15]);
                }
            }

            MessageBox.Show("Done");
        }

        private void chooseDirButton_Click(object sender, EventArgs e)
        {
            var dlg = new FolderBrowserDialog();
            dlg.ShowDialog();
            sourcePathTextbox.Text = dlg.SelectedPath;
        }

        private void chooseDestinationButton_Click(object sender, EventArgs e)
        {
            var dlg = new SaveFileDialog();
            dlg.ShowDialog();
            destPathTextbox.Text = dlg.FileName;
        }
    }
}
