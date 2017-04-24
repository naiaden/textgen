# Retain only sentences. from paragraphs that end with punctuation.

import collections
import csv
import random
from localdefs import *

LEXICON_FILE = str(DATA_DIR / 'lexicon.csv')
SJABLOON_FILE = str(DATA_DIR / 'sjabloon.txt')

LEXICON_HEADER = ['TOKEN', 'POSTAG', 'FREQUENCY']

class Sjablonen:

    def __init__(self):
        with open(SJABLOON_FILE, encoding='utf-8') as source:
            self.data = [line.split() for line in source]

    def random(self):
        return random.choice(self.data)

class Lexicon:

    def __init__(self):
        self.data = collections.defaultdict(set)
        with open(LEXICON_FILE, encoding='utf-8') as source:
            reader = csv.reader(source, dialect='local')
            assert next(reader) == LEXICON_HEADER
            for token, postag, frequency in reader:
                self.data[postag].add((int(frequency), token))
        for postag in self.data:
            total = sum(x[0] for x in self.data[postag])
            tokens = sorted(self.data[postag], reverse=True)
            self.data[postag] = (total, tokens)

    def random(self, postag):
        total, tokens = self.data[postag]
        x = random.randrange(total)
        count = 0
        for frequency, token in tokens:
            count += frequency
            if count > x:
                return token

def main():
    sjablonen = Sjablonen()
    lexicon = Lexicon()
    # Genereer maffe tekst
    print()
    for s in range(10):
        sjabloon = sjablonen.random()
        sentence = []
        for item in sjabloon:
            if '(' in item and item.endswith(')'):
                # Postag: select a random token
                sentence.append(lexicon.random(item))
            else:
                # Punctuation
                sentence.append(item)
        sentence = ' '.join(sentence)
        sentence = sentence[:1].upper() + sentence[1:]
        sentence = sentence.replace(' .', '.')
        sentence = sentence.replace(' ,', ',')
        sentence = sentence.replace(' :', ':')
        sentence = sentence.replace(' ;', ';')
        sentence = sentence.replace(' !', '!')
        sentence = sentence.replace(' ?', '?')
        sentence = sentence.replace(' )', ')')
        sentence = sentence.replace('( ', '(')
        print(sentence, end=' ')
    print('\n')

if __name__ == '__main__':
    main()
