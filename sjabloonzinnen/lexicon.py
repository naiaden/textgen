# Retain only sentences. from paragraphs that end with punctuation.

import collections
import csv
from localdefs import *

SOURCE_FILE = str(DATA_DIR / 'sentences.csv')
TARGET_FILE = str(DATA_DIR / 'lexicon.csv')

SOURCE_HEADER = ['TOKEN', 'POSTAG']
TARGET_HEADER = ['TOKEN', 'POSTAG', 'FREQUENCY']

def main():
    print('Reading {}'.format(SOURCE_FILE))
    with open(SOURCE_FILE, encoding='utf-8') as source:
        reader = csv.reader(source, dialect='local')
        assert next(reader) == SOURCE_HEADER
        x = collections.Counter()
        for token, postag in reader:
            if not token and not postag: continue
            x[(token, postag)] += 1
    print('Writing {}'.format(TARGET_FILE))
    with open(TARGET_FILE, 'w', encoding='utf-8') as target:
        writer = csv.writer(target, dialect='local')
        writer.writerow(TARGET_HEADER)
        for (token, postag), frequency in x.items():
            writer.writerow([token, postag, frequency])

if __name__ == '__main__':
    main()
