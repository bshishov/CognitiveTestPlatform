using System.IO;
using Newtonsoft.Json;
using Shine;

namespace PsycologicalWebTest
{
    class Test
    {
        [JsonProperty("id")]
        public string Id { get; set; }

        [JsonProperty("name")]
        public string Name { get; set; }

        [JsonProperty("version")]
        public string Vesrion { get; set; }

        [JsonProperty("instructions")]
        public string Instructions { get; set; }

        [JsonProperty("record_audio")]
        public bool RecordAudio { get; set; }

        [JsonProperty("record_video")]
        public bool RecordVideo { get; set; }

        [JsonProperty("record_mouse")]
        public bool RecordMouse { get; set; }

        [JsonProperty("scripts")]
        public string[] Scripts { get; set; }


        public virtual void Save(string baseFolder, Participant p, IRequest request)
        {
            var dir = Path.Combine(baseFolder, p.FolderName, $"{Id}_v{Vesrion}", "raw");
            if (!Directory.Exists(dir))
                Directory.CreateDirectory(dir);

            foreach (var filePart in request.Files)
            {
                using (var file = File.OpenWrite(Path.Combine(dir, filePart.FileName)))
                {
                    filePart.Data.CopyTo(file);
                }
            }

            if (!string.IsNullOrEmpty(request.PostArgs["mouse_events"]))
                File.WriteAllText(Path.Combine(dir, "mouse_events.json"), request.PostArgs["mouse_events"]);

            if (!string.IsNullOrEmpty(request.PostArgs["events"]))
                File.WriteAllText(Path.Combine(dir, "events.json"), request.PostArgs["events"]);
        }
    }
}
