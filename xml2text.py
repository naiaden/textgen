

import sys
from bs4 import BeautifulSoup

infile = sys.argv[1]
outfile = sys.argv[2]

with open(infile,'r',encoding='utf-8') as file_in:
    file_str = file_in.read()
    souped = BeautifulSoup(file_str)

text = souped.text
with open(outfile,'w',encoding='utf-8') as out:
    out.write(text)
