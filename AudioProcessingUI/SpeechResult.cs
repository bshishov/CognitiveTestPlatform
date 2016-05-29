using System.ComponentModel;
using System.Data;
using System.Linq;
using System.Numerics;
using System.Text;
using System.Threading.Tasks;
using Accord.Audio.Generators;
using Accord.Audio.Windows;
using Accord.Controls;
using Accord.Math;
using Accord.Statistics;
using Accord.Statistics.Testing;
using AForge;
using AForge.Math;

namespace AudioProcessingUI
{
    struct SpeechResult
    {
        public double F0Mean;
        public double F0Std;
        public double Jitter;
        public double Shimmer;
        public double HFEnergy;
    }
}
