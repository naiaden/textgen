# Retain only sentences. from paragraphs that end with punctuation.

import collections
import csv
import random

from distribution import Distribution
from localdefs import *

N = 10    # Length of N-grams
W = 200   # Length of text to generate

TOKEN_FILE = str(DATA_DIR / 'tokens.csv')
LEXICON_FILE = str(DATA_DIR / 'lexicon.csv')

TOKEN_HEADER = ['SONAR-ID', 'TOKEN', 'POSTAG']
LEXICON_HEADER = ['TOKEN', 'POSTAG', 'FREQUENCY']

def get_lexicon():
    lexicon = collections.defaultdict(dict)
    with open(LEXICON_FILE, encoding='utf-8') as source:
        reader = csv.reader(source, dialect='local')
        assert next(reader) == LEXICON_HEADER
        for token, postag, frequency in reader:
            lexicon[postag][token] = int(frequency)
    for postag in lexicon:
        lexicon[postag] = Distribution(lexicon[postag])
    # Fix for newlines
    lexicon['PARA()'].values[0] = '\n'
    return lexicon

def get_ngrams():
    ngrams = collections.defaultdict(collections.Counter)
    with open(TOKEN_FILE, encoding='utf-8') as source:
        reader = csv.reader(source, dialect='local')
        assert next(reader) == TOKEN_HEADER
        overlap = ()
        while len(overlap) < N - 1:
            sonar_id, token, postag = next(reader)
            if postag == 'LET()': postag = token
            overlap += (postag,)
        for sonar_id, token, postag in reader:
            if postag == 'LET()': postag = token
            ngrams[overlap][postag] += 1
            overlap = overlap[1:] + (postag,)
    for overlap in ngrams:
        ngrams[overlap] = Distribution(ngrams[overlap])
    return ngrams

def main():
    ngrams = get_ngrams()
    lexicon = get_lexicon()

    # Genereer maffe tekst
    text = []
    overlap = random.choice(list(ngrams.keys()))
    for w in range(W):
        postag = ngrams[overlap].choice()
        token = lexicon[postag].choice()
        if overlap[-1] in ('.', '?', '!', 'PARA()'):
            token = token[0].upper() + token[1:]
        text.append(token)
        overlap = overlap[1:] + (postag,)
    # Postprocessing
    text = ' '.join(text)
    text = text.replace('\n ', '\n')
    text = text.replace('\n\' ', '\n\'')
    text = text.replace(' \'\n', '\'\n')
    text = text.replace('. \'', '.\'')
    text = text.replace(', \'', ',\'')
    for symbol in '.,:;!?)':
        text = text.replace(' ' + symbol, symbol)
    for symbol in '(':
        text = text.replace(symbol + ' ', symbol)
    text = text.replace('\n', '\n    ')
    print(text)

if __name__ == '__main__':
    main()
