# Retain only sentences. from paragraphs that end with punctuation.

import collections
import csv
from localdefs import *

SOURCE_FILE = str(DATA_DIR / 'tokens.csv')
TARGET_FILE = str(DATA_DIR / 'lexicon.csv')

SOURCE_HEADER = ['SONAR-ID', 'TOKEN', 'POSTAG']
TARGET_HEADER = ['TOKEN', 'POSTAG', 'FREQUENCY']

def main():
    print('Reading {}'.format(SOURCE_FILE))
    with open(SOURCE_FILE, encoding='utf-8') as source:
        reader = csv.reader(source, dialect='local')
        assert next(reader) == SOURCE_HEADER
        x = collections.Counter()
        for sonar_id, token, postag in reader:
            if postag == 'LET()':
                postag = token
            if 'eigen' not in postag and not postag.startswith('SPEC('):
                token = token.lower()
            x[(token, postag)] += 1

    # Sort by frequency, then by postag, then by token
    data = sorted(x.items(), key=lambda z: (-z[1], z[0][1], z[0][0]))

    print('Writing {}'.format(TARGET_FILE))
    with open(TARGET_FILE, 'w', encoding='utf-8') as target:
        writer = csv.writer(target, dialect='local')
        writer.writerow(TARGET_HEADER)
        for (token, postag), frequency in data:
            writer.writerow([token, postag, frequency])

if __name__ == '__main__':
    main()
