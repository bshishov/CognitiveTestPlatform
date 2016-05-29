using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;

namespace Shared
{
    public class CsvWriter : IDisposable
    {
        private readonly StreamWriter _writer;

        public CsvWriter(string path, params string[] header)
        {
            _writer = new StreamWriter(path);


            if (header.Length > 0)
            {
                _writer.Write(String.Join(",", header) + "\n");
            }
        }

        public void Write(params object[] values)
        {
            if(values.Length == 0)
                throw new ArgumentException("No values");

            var strings = new List<string>();
            foreach (var value in values)
            {
                if(value == null)
                    strings.Add(string.Empty);
                else if(value is string)
                    strings.Add(S((string)value));
                else if (value is double)
                    strings.Add(S((double)value));
                else if (value is float)
                    strings.Add(S((float)value));
                else if (value is int)
                    strings.Add(S((int)value));
                else
                    strings.Add(S(value.ToString()));
            }

            _writer.Write(String.Join(",", strings) + "\n");
        }
        
        private string S(int val)
        {
            return val.ToString(CultureInfo.InvariantCulture);
        }

        private string S(double val)
        {
            return val.ToString(CultureInfo.InvariantCulture);
        }

        private string S(float val)
        {
            return val.ToString(CultureInfo.InvariantCulture);
        }

        private string S(string s)
        {
            return $"\"{s}\"";
        }

        public void Dispose()
        {
            _writer.Close();
            _writer.Dispose();
        }
    }
}