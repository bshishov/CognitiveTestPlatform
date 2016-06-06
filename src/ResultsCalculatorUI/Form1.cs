using System;
using System.Collections;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Newtonsoft.Json;
using ResultsCalculator;
using Shared;

namespace ResultsCalculatorUI
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            var testsFolder = "D:\\results\\";
            var participantsRaw = JsonConvert.DeserializeObject(File.ReadAllText(Path.Combine(testsFolder, "participants.json")));

            var participants = ((IEnumerable) participantsRaw).Cast<dynamic>();

            using (var csv = new CsvWriter(Path.Combine(testsFolder, "results.csv"), typeof(SummaryResults)))
            {
                foreach (var participant in participants)
                {
                    var folder = (string)participant.FolderName;
                    var path = Path.Combine(testsFolder, folder);

                    if(!Directory.Exists(path))
                        continue;

                    var calc = new ResultsCalculator.ResultsCalculator(path);

                    var initial = new SummaryResults()
                    {
                        Id = (int)participant.Id,
                        FolderName = (string)participant.FolderName,
                        Name = (string)participant.Name,
                        Age =(int) participant.Age
                    };

                    var res = calc.Compute(initial);
                    csv.WriteObject(res);
                }
            }
        }
    }
}
