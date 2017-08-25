
import sys
import json

import featuregenerator

outfile = sys.argv[1]
frogconfig = sys.argv[2]
txtfiles = sys.argv[3:]

all_sentences = []
for txtfile in txtfiles:
    all_sentences.extend(featuregenerator.frog_txt(txtfile,frogconfig))

with open(outfile,'w',encoding='utf-8') as out:
    for sentence in all_sentences:
        json.dump(sentence,out)
        out.write('\n')
