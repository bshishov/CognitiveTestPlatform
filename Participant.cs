using System;

namespace PsycologicalWebTest
{
    class Participant
    {
        public int Id;
        public int LastTest;
        public string Session;
        public string Name;
        public int Age;
        public int Gender;
        public string Allow;
        public string FolderName => $"{Id}-{Created.ToShortDateString()}";
        public DateTime Created = DateTime.Now;
    }
}