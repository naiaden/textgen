# Retain only sentences. from paragraphs that end with punctuation.

import csv
from localdefs import *

SOURCE_FILE = str(DATA_DIR / 'tokens.csv')
TARGET_FILE = str(DATA_DIR / 'sentences.csv')

SOURCE_HEADER = ['SONAR-ID', 'TOKEN', 'POSTAG']
TARGET_HEADER = ['TOKEN', 'POSTAG']

def main():
    print('Reading {}'.format(SOURCE_FILE))
    print('Writing {}'.format(TARGET_FILE))
    with open(SOURCE_FILE, encoding='utf-8') as source:
        reader = csv.reader(source, dialect='local')
        assert next(reader) == SOURCE_HEADER
        with open(TARGET_FILE, 'w', encoding='utf-8') as target:
            writer = csv.writer(target, dialect='local')
            writer.writerow(TARGET_HEADER)
            sentence = []
            for sonar_id, token, postag in reader:
                if 'eigen' not in postag: token = token.lower()
                if token.startswith('«'): token = token[1:]
                if token.endswith('»'): token = token[:-1]
                ids = sonar_id.split('.')
                if ids[1] != 'p': continue
                if ids[-1] == '1':
                    if sentence and len(sentence) > 1 and sentence[-1][1] == 'LET()':
                        for row in sentence:
                            writer.writerow(row)
                        writer.writerow(['', ''])
                    sentence = []
                sentence.append((token, postag))
            if len(sentence) > 1 and sentence[-1][1] == 'LET()':
                for token, postag in sentence:
                    writer.writerow([token, postag])
                writer.writerow(['', ''])

if __name__ == '__main__':
    main()
