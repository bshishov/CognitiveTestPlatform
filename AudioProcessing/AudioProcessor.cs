using System.IO;

namespace AudioProcessing
{
    public class AudioProcessor
    {
       

        public AudioProcessor(string wavPath)
        {
            using (var reader = new BinaryReader(File.OpenRead(wavPath)))
            {
                
            }
        }
    }
}
