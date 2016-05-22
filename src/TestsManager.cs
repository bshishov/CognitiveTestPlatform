using System.Collections.Generic;
using System.IO;
using System.Linq;
using Newtonsoft.Json;

namespace PsycologicalWebTest
{
    class TestsManager
    {
        public string BaseFolder { get; }

        public IEnumerable<Test> Tests => _tests;

        private readonly List<Test> _tests;

        public TestsManager(string tests, string baseFolder)
        {
            BaseFolder = baseFolder;
            _tests = JsonConvert.DeserializeObject<List<Test>>(File.ReadAllText(tests));

            if (!Directory.Exists(BaseFolder))
                Directory.CreateDirectory(BaseFolder);
        }

        public Test GetById(string id)
        {
            return _tests.FirstOrDefault(t => t.Id.Equals(id));
        }

        public Test GetNextFor(Test last)
        {
            var index = _tests.IndexOf(last) + 1;
            if (index >= _tests.Count)
                return null;

            return _tests[index];
        }
    }
}