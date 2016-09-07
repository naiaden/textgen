# Retain only sentences. from paragraphs that end with punctuation.

import collections
import csv
import random

from distribution import Distribution
from localdefs import *

N_postag = 10    # Length of postag shingles
N_token = 2      # Length of token shingles
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

def get_postag_shingles():
    shingles = collections.defaultdict(collections.Counter)
    with open(TOKEN_FILE, encoding='utf-8') as source:
        reader = csv.reader(source, dialect='local')
        assert next(reader) == TOKEN_HEADER
        shingle = ()
        while len(shingle) < N_postag - 1:
            sonar_id, token, postag = next(reader)
            if postag == 'LET()': postag = token
            shingle += (postag,)
        for sonar_id, token, postag in reader:
            if postag == 'LET()': postag = token
            shingles[shingle][postag] += 1
            shingle = shingle[1:] + (postag,)
    for shingle in shingles:
        shingles[shingle] = Distribution(shingles[shingle])
    return shingles

def get_token_shingles():
    shingles = collections.defaultdict(collections.Counter)
    with open(TOKEN_FILE, encoding='utf-8') as source:
        reader = csv.reader(source, dialect='local')
        assert next(reader) == TOKEN_HEADER
        # Get start shingle (token, postag)
        _s, prev_token, _p = next(reader)
        #
        for _s, token, postag in reader:
            if postag == 'LET()': postag = token
            shingle = (prev_token, postag)
            shingles[shingle][token] += 1
            prev_token = token
    for shingle in shingles:
        shingles[shingle] = Distribution(shingles[shingle])
    return shingles

def main():
    postag_shingles = get_postag_shingles()
    token_shingles = get_token_shingles()
    # Genereer een tekst bestaande uit postags
    postag_text = []
    shingle = random.choice(list(postag_shingles.keys()))
    for w in range(W):
        postag = postag_shingles[shingle].choice()
        postag_text.append(postag)
        shingle = shingle[1:] + (postag,)

    # Kies een token voor elke postag
    postag = None
    while postag != postag_text[0]:
        token, postag = random.choice(list(token_shingles.keys()))
    token_text = [token]
    while len(token_text) < len(postag_text):
        shingle = token_text[-1], postag_text[len(token_text)]
        print(len(token_text), shingle)
        if shingle in token_shingles:
            token = token_shingles[shingle].choice()
            token_text.append(token)
            # print('  =>', token, postag_text[len(token_text)])
        else:
            while True:
                del token_text[-1]
                shingle = token_text[-1], postag_text[len(token_text)]
                if len(token_shingles[shingle].values) > 1: break

    # Postprocessing
    text = ' '.join(token_text)
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
