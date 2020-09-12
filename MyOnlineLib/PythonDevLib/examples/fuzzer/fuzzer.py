#C:\Python27\python.exe C:\Users\ndhavalikar\Desktop\fuzzer.py
#C:\Python27\Scripts\pip.exe install Intro_Testing
from fuzzingbook.Fuzzer import RandomFuzzer

f = RandomFuzzer()
print(f.fuzz())

###Produce strings of `min_length` to `max_length` characters in the range [`char_start`, `char_start` + `char_range`]
random_fuzzer = RandomFuzzer(min_length=10, max_length=20, char_start=65, char_range=26)
print (random_fuzzer.fuzz())