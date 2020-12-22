using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using System.Diagnostics;
using System.IO;
using System.Security.Cryptography;


namespace MyCrypto
{
    public static class Cryptography
    {
        private static void MakeKeyAndIV(string password, byte[] salt, int key_size_bits, int block_size_bits, out byte[] key, out byte[] iv)
        {
            Rfc2898DeriveBytes derive_bytes = new Rfc2898DeriveBytes(password, salt, 1000);

            key = derive_bytes.GetBytes(key_size_bits / 8);
            iv = derive_bytes.GetBytes(block_size_bits / 8);
        }

        public static void EncryptFile(string password, string in_file, string out_file)
        {
            CryptFile(password, in_file, out_file, true);
        }
        public static void DecryptFile(string password, string in_file, string out_file)
        {
            CryptFile(password, in_file, out_file, false);
        }
        public static void CryptFile(string password, string in_file, string out_file, bool encrypt)
        {
            using (FileStream in_stream = new FileStream(in_file, FileMode.Open, FileAccess.Read))
            {
                using (FileStream out_stream = new FileStream(out_file, FileMode.Create, FileAccess.Write))
                {
                    CryptStream(password, in_stream, out_stream, encrypt);
                }
            }
        }

        public static void CryptStream(string password, Stream in_stream, Stream out_stream, bool encrypt)
        {
            AesCryptoServiceProvider aes_provider = new AesCryptoServiceProvider();

            int key_size_bits = 0;
            for (int i = 1024; i > 1; i--)
            {
                if (aes_provider.ValidKeySize(i))
                {
                    key_size_bits = i;
                    break;
                }
            }
            Debug.Assert(key_size_bits > 0);
            Console.WriteLine("Key size: " + key_size_bits);

            int block_size_bits = aes_provider.BlockSize;

            byte[] key = null;
            byte[] iv = null;
            byte[] salt = { 0x0, 0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0xF1, 0xF0, 0xEE, 0x21, 0x22, 0x45 };
            MakeKeyAndIV(password, salt, key_size_bits, block_size_bits, out key, out iv);

            ICryptoTransform crypto_transform;
            if (encrypt)
            {
                crypto_transform = aes_provider.CreateEncryptor(key, iv);
            }
            else
            {
                crypto_transform = aes_provider.CreateDecryptor(key, iv);
            }

            try
            {
                using (CryptoStream crypto_stream = new CryptoStream(out_stream, crypto_transform, CryptoStreamMode.Write))
                {
                    const int block_size = 1024;
                    byte[] buffer = new byte[block_size];
                    int bytes_read;
                    while (true)
                    {
                        bytes_read = in_stream.Read(buffer, 0, block_size);
                        if (bytes_read == 0) break;

                        crypto_stream.Write(buffer, 0, bytes_read);
                    }
                }
            }
            catch { }

            crypto_transform.Dispose();
        }

        public static byte[] CryptBytes(string password, byte[] in_bytes, bool encrypt)
        {
            AesCryptoServiceProvider aes_provider = new AesCryptoServiceProvider();

            int key_size_bits = 0;
            for (int i = 1024; i > 1; i--)
            {
                if (aes_provider.ValidKeySize(i))
                {
                    key_size_bits = i;
                    break;
                }
            }
            Debug.Assert(key_size_bits > 0);
            Console.WriteLine("Key size: " + key_size_bits);

            int block_size_bits = aes_provider.BlockSize;

            byte[] key = null;
            byte[] iv = null;
            byte[] salt = { 0x0, 0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0xF1, 0xF0, 0xEE, 0x21, 0x22, 0x45 };
            MakeKeyAndIV(password, salt, key_size_bits, block_size_bits, out key, out iv);

            ICryptoTransform crypto_transform;
            if (encrypt)
            {
                crypto_transform = aes_provider.CreateEncryptor(key, iv);
            }
            else
            {
                crypto_transform = aes_provider.CreateDecryptor(key, iv);
            }

            using (MemoryStream out_stream = new MemoryStream())
            {
                using (CryptoStream crypto_stream = new CryptoStream(out_stream,
                    crypto_transform, CryptoStreamMode.Write))
                {
                    crypto_stream.Write(in_bytes, 0, in_bytes.Length);
                    try
                    {
                        crypto_stream.FlushFinalBlock();
                    }
                    catch (CryptographicException) { }

                    catch { throw; }

                    return out_stream.ToArray();
                }
            }
        }

        public static byte[] Encrypt(this string the_string, string password)
        {
            System.Text.ASCIIEncoding ascii_encoder = new System.Text.ASCIIEncoding();
            byte[] plain_bytes = ascii_encoder.GetBytes(the_string);
            return CryptBytes(password, plain_bytes, true);
        }

        public static string Decrypt(this byte[] the_bytes, string password)
        {
            byte[] decrypted_bytes = CryptBytes(password, the_bytes, false);
            System.Text.ASCIIEncoding ascii_encoder = new System.Text.ASCIIEncoding();
            return ascii_encoder.GetString(decrypted_bytes);
        }

        public static string CryptString(string password, string in_string, bool encrypt)
        {
            byte[] in_bytes = Encoding.ASCII.GetBytes(in_string);
            using (MemoryStream in_stream = new MemoryStream(in_bytes))
            {
                using (MemoryStream out_stream = new MemoryStream())
                {
                    CryptStream(password, in_stream, out_stream, true);

                    out_stream.Seek(0, SeekOrigin.Begin);
                    using (StreamReader stream_reader = new StreamReader(out_stream))
                    {
                        return stream_reader.ReadToEnd();
                    }
                }
            }
        }

        public static string ToHex(this byte[] the_bytes)
        {
            return ToHex(the_bytes, false);
        }
        public static string ToHex(this byte[] the_bytes, bool add_spaces)
        {
            string result = "";
            string separator = "";
            if (add_spaces) separator = " ";
            for (int i = 0; i < the_bytes.Length; i++)
            {
                result += the_bytes[i].ToString("x2") + separator;
            }
            return result;
        }

        public static byte[] ToBytes(this string the_string)
        {
            List<byte> the_bytes = new List<byte>();
            the_string = the_string.Replace(" ", "");

            for (int i = 0; i < the_string.Length; i += 2)
            {
                the_bytes.Add(
                    byte.Parse(the_string.Substring(i, 2),
                        System.Globalization.NumberStyles.HexNumber));
            }
            return the_bytes.ToArray();
        }
    }
}
