# Writers in the Cloud
#
#
import configparser
import json
import random

from languagemodel import LanguageModel
from textgenerator import TextGenerator
from normaliser import FrogNormaliser
from sentence_semantics import SentenceSemantics

config = configparser.ConfigParser()
config.read('witc.ini')

cache_file = config['INPUT']['CacheFile']
minimum_paragraph_length = int(config['OUTPUT'].get('MinimumParagraphLength', 30))
w2v_model = config['INPUT']['W2V']
testout = config['OUTPUT']['StoryFile']

if cache_file:
    print("+ Reading cache file")
    with open(cache_file) as data_file:
        data = json.load(data_file)

print("+ Normalising frogged data")
fn = FrogNormaliser(data)

print("+ Creating language model")
lm = LanguageModel(data)

print("+ Loading Word2Vec model")
ss = SentenceSemantics()
ss.load_model(w2v_model)

print("+ Generating text")
tg = TextGenerator(lm, minimum_paragraph_length)
with open(testout,'w',encoding='utf-8') as t_out:
    target = tg.generate_sentence()
    t_out.write('start : ' + ' '.join(target) + '\n')
    for i in range(50):
        sources = [tg.generate_sentence() for x in range(150)]
        candidates = ss.return_sentence_candidates(target,sources)
        target = random.choice([x[0] for x in candidates])
        t_out.write(str(i) + ' : ' + ' '.join(target) + '\n')

#print(tg.generate_paragraph()) 

