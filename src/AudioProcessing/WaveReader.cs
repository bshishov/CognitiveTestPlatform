using System;
using System.IO;
using Accord.Audio;
using Accord.Audio.Formats;

namespace AudioProcessing
{
    public class WaveReader : IAudioDecoder, IDisposable
    {
        public SampleFormat Format { get; private set; }
        public short BlockAlign { get; private set; }
        public int DataSize { get; private set; }
        public short Channels{ get; private set; }
        public int SampleRate { get; private set; }

        private BinaryReader _reader;

        public WaveReader()
        {
        }

        public int Open(Stream stream)
        {
            _reader = new BinaryReader(stream);
            int chunkId = _reader.ReadInt32();
            int chunkSize = _reader.ReadInt32();

            // Содержит символы “WAVE” (0x57415645 в big-endian представлении)
            int format = _reader.ReadInt32();

            // Содержит символы “fmt “ (0x666d7420 в big-endian представлении)
            int subchunk1Id = _reader.ReadInt32();

            // 16 для формата PCM. Это оставшийся размер подцепочки, начиная с этой позиции.
            int subchunk1Size = _reader.ReadInt32();

            // Аудио формат, полный список можно получить здесь. Для PCM = 1 (то есть, Линейное квантование). Значения, отличающиеся от 1, обозначают некоторый формат сжатия.
            int audioFormat = _reader.ReadInt16();

            // Количество каналов. Моно = 1, Стерео = 2 и т.д.
            Channels = _reader.ReadInt16();

            // Частота дискретизации. 8000 Гц, 44100 Гц и т.д.
            SampleRate = _reader.ReadInt32();

            // Количество байт, переданных за секунду воспроизведения.
            int byteRate = _reader.ReadInt32();

            // Количество байт для одного сэмпла, включая все каналы.
            BlockAlign = _reader.ReadInt16();

            // Количество бит в сэмпле. Так называемая “глубина” или точность звучания. 8 бит, 16 бит и т.д.
            int bitDepth = _reader.ReadInt16();


            if (subchunk1Size == 18)
            {
                // Read any extra values
                int fmtExtraSize = _reader.ReadInt16();
                _reader.ReadBytes(fmtExtraSize);
            }

            int dataID = _reader.ReadInt32();
            DataSize = _reader.ReadInt32();

            var sampleFormat = SampleFormat.Format16Bit;

            // if WAVE_FORMAT_IEEE_FLOAT
            if (audioFormat == 3)
            {
                if (bitDepth == 32)
                    sampleFormat = SampleFormat.Format32BitIeeeFloat;
                if (bitDepth == 64)
                    sampleFormat = SampleFormat.Format64BitIeeeFloat;
            }
            else if (audioFormat == 1) // if WAVE_FORMAT_PCM
            {
                if (bitDepth == 8)
                    sampleFormat = SampleFormat.Format8Bit;
                if (bitDepth == 16)
                    sampleFormat = SampleFormat.Format16Bit;
                if (bitDepth == 32)
                    sampleFormat = SampleFormat.Format32Bit;
            }

            Format = sampleFormat;
            return 0;
        }

        public Signal Decode()
        {
            var frames = DataSize / BlockAlign;
            var bufferSize = Channels * frames;

            var floatBuffer = new float[bufferSize];
            switch (Format)
            {
                case SampleFormat.Format8Bit: // Stream is 8 bits
                    {
                        byte[] block = _reader.ReadBytes(bufferSize);
                        SampleConverter.Convert(block, floatBuffer);
                    }
                    break;

                case SampleFormat.Format16Bit: // Stream is 16 bits
                    {
                        short[] block = new short[bufferSize];

                        for (int i = 0; i < bufferSize; i++)
                            block[i] = _reader.ReadInt16();
                        SampleConverter.Convert(block, floatBuffer);
                    }
                    break;
                case SampleFormat.Format32Bit: // Stream is 32 bits
                    {
                        int[] block = new int[bufferSize];

                        for (int i = 0; i < bufferSize; i++)
                            block[i] = _reader.ReadInt32();
                        SampleConverter.Convert(block, floatBuffer);
                    }
                    break;
                case SampleFormat.Format32BitIeeeFloat:
                    {
                        float[] block = new float[bufferSize];

                        for (int i = 0; i < bufferSize; i++)
                            block[i] = _reader.ReadInt32();
                        floatBuffer = block;
                    }
                    break;
                default:
                    throw new NotSupportedException($"Format {Format} is unsupported");
            }

            return Signal.FromArray(floatBuffer, Channels, SampleRate, SampleFormat.Format32BitIeeeFloat);
        }

        public Signal Decode(int index, int frames)
        {
            throw new NotImplementedException();
        }

        public void Close()
        {
            _reader.Close();
        }

        public void Dispose()
        {
            _reader.Dispose();
        }
    }
}