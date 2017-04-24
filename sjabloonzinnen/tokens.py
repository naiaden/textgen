# Extract tokens literatim from SoNaR-500.
# The program has a -tN option to stop extraction after N tokens.

import csv
import getopt
import pathlib
import xml.etree.ElementTree
import sys
from localdefs import *

PARAMS_FILE = str(DATA_DIR / 'sonardir.csv')
TARGET_FILE = str(DATA_DIR / 'tokens.csv')

PARAMS_HEADER = ['QUALITY', 'SKIP', 'SUBJECT', 'FILE-COUNT', 'BYTE-COUNT', 'SONAR-DIR']
TARGET_HEADER = ['SONAR-ID', 'TOKEN', 'POSTAG']

def main():
    max_tokens = parse_arguments()
    extract(max_tokens)

def parse_arguments():
    max_tokens = None
    optlist, xargs = getopt.getopt(sys.argv[1:], 't:')
    for opt, arg in optlist:
        if opt == '-t':
            max_tokens = int(arg)
    return max_tokens

def extract(max_tokens):
    print('Reading {}'.format(SONAR_DIR))
    print('Writing {}'.format(TARGET_FILE))
    with open(TARGET_FILE, 'w', encoding='utf-8') as target:
        writer = csv.writer(target, dialect='local')
        writer.writerow(TARGET_HEADER)
        num_tokens = 0
        with open(PARAMS_FILE, encoding='utf-8') as params:
            reader = csv.reader(params, dialect='local')
            assert next(reader) == PARAMS_HEADER
            for _q, skip, subject, _f, _b, sonar_dir in reader:
                if skip: continue
                print('  {}'.format(subject))
                for filename in pathlib.Path(sonar_dir).glob('*.xml'):
                    tree = xml.etree.ElementTree.parse(str(filename))
                    for w in tree.iter('{http://ilk.uvt.nl/folia}w'):
                        sonar_id = w.get('{http://www.w3.org/XML/1998/namespace}id')
                        token = w.find('{http://ilk.uvt.nl/folia}t').text
                        postag = w.find('{http://ilk.uvt.nl/folia}pos').get('class')
                        writer.writerow([sonar_id, token, postag])
                        num_tokens += 1
                    print(num_tokens, end='\r')
                    if max_tokens and num_tokens > max_tokens:
                        exit()

if __name__ == '__main__':
    main()
