
import sys
import json

import sentence_semantics

"""
Script to load files with pos-tagged sentences in json-format and train a w2v model
""" 

model_out = sys.argv[1]
json_corpora = sys.argv[2:]

sentences = []

# load in sentences
for json_corpus in json_corpora:
    print('loading in sentences for',json_corpus)
    with open(json_corpus,'r',encoding='utf-8') as corpus_in:
        corpus_str = corpus_in.read()
    corpus_json = json.loads(corpus_str)
    sentences.extend([[token['word'] for token in sentence if token['pos'] != 'LET()'] for sentence in corpus_json])

print('done. loaded',len(sentences),'sentences')

print('now training w2v model...')
sensem = sentence_semantics.SentenceSemantics()
sensem.train_model(sentences)

print('done. saving model...')
sensem.save_model(model_out)
