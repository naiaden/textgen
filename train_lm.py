
import languagemodel
import json
import sys
import random

infile = sys.argv[1]  # feats.json file
out_lm = sys.argv[2]  # the name of the lm to save

print('reading file')
with open(infile,'r',encoding='utf-8') as f_in:
    file_lines = f_in.read().strip().split('\n')
sentences = [json.loads(line) for line in file_lines]

print('training language model')
lm = languagemodel.LanguageModel()
lm.train_model(sentences)

print('saving language model')
lm.save_model(out_lm)
