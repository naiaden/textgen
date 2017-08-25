
import json

import featuregenerator

sentences = featuregenerator.frog_txt('/vol/bigdata2/corpora2/Couperus/couperus.plain.txt')
print(sentences[:4])

with open('couperus_feats.json','w',encoding='utf-8') as wout:
    json.dump(sentences, wout)
