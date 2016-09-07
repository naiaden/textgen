# Retain only sentences. from paragraphs that end with punctuation.

import csv
from localdefs import *

SOURCE_FILE = str(DATA_DIR / 'sentences.csv')
TARGET_FILE = str(DATA_DIR / 'sjabloon.txt')

SOURCE_HEADER = ['TOKEN', 'POSTAG']

def main():
    print('Reading {}'.format(SOURCE_FILE))
    print('Writing {}'.format(TARGET_FILE))
    with open(SOURCE_FILE, encoding='utf-8') as source:
        reader = csv.reader(source, dialect='local')
        assert next(reader) == SOURCE_HEADER
        sjabloon = []
        with open(TARGET_FILE, 'w', encoding='utf-8') as target:
            for token, postag in reader:
                if token or postag:
                    sjabloon.append(token if postag == 'LET()' else postag)
                else:
                    if sjabloon:
                        target.write(' '.join(sjabloon))
                        target.write('\n')
                    sjabloon = []
            assert not sjabloon

if __name__ == '__main__':
    main()
