using System.Collections.Generic;
using System.IO;
using System.Linq;
using Newtonsoft.Json;

namespace PsycologicalWebTest
{
    class ParticipantManager
    {
        public IEnumerable<Participant> Participants => _participants;

        private List<Participant> _participants = new List<Participant>();
        private readonly string _fileName;

        public ParticipantManager(string fileName)
        {
            _fileName = fileName;
            Load();
        }

        public void Add(Participant participant)
        {
            if(_participants.Count > 0)
                participant.Id = _participants.Max(p => p.Id) + 1; // Auto increment
            else
                participant.Id = 1;
            _participants.Add(participant);
            Save();
        }

        private void Load()
        {
            if (!File.Exists(_fileName))
                return;
            
            _participants = JsonConvert.DeserializeObject<List<Participant>>(File.ReadAllText(_fileName));
            if(_participants == null)
                _participants = new List<Participant>();
        }

        public void Save()
        {
            File.WriteAllText(_fileName, JsonConvert.SerializeObject(_participants, new JsonSerializerSettings()
            {
                Formatting = Formatting.Indented,
            }));
        }

        public Participant GetBySession(string session)
        {
            if(_participants != null && _participants.Count > 0)
                return _participants.LastOrDefault(p => p.Session.Equals(session));

            return null;
        }
    }
}
