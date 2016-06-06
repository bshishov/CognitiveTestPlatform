using System;

namespace PsycologicalWebTest
{
    class Participant
    {
        public int Id { get; set; }
        public int LastTest { get; set; }
        public string Session { get; set; }
        public string Name { get; set; }
        public int Age { get; set; }
        public int Gender { get; set; }
        public string Allow { get; set; }
        public string FolderName => $"{Id}-{Created.ToString("dd-MM-yy")}";
        public DateTime Created = DateTime.Now;
        public string Email { get; set; }
    }
}