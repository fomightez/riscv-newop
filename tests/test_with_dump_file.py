import os
import pytest
import string
from bitarray import bitarray
from rvnewop import RV32

class DumpFileReader:
    def __init__(self, file_name):
        rv = RV32("32IC")
        if os.path.exists(file_name) == False:
            print ("Fatal: Unable to find the file: " + file_name)
        else:
            df_handle = open(file_name, 'r')
            lines = df_handle.readlines()
            for line in lines:
                words = line.split()
                # Look for lines with at least 4 space-separated words
                if len(words) > 3:
                    # PC is recorded in the dump file with syntac <PC>:
                    # Strip the : away
                    words[0]=words[0].replace(':','')

                    # Some false matches such as the line "Disassembly of section .text:"
                    # Remove those by ensuring that the first word is a valid hex value
                    if all(c in string.hexdigits for c in words[0]):
                        instruction_word = words[1]
                        decoded_str = str(rv.decodeHex(instruction_word)).split()
                        assert decoded_str[0] == words[2]
                        

def test_dump_file():
    DumpFileReader("sample.dump")
    assert True
