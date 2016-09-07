import csv
import os
from pathlib import Path
from localdefs import *

SOURCE_DIR = SONAR_DIR
TARGET_FILE = str(DATA_DIR / 'sonardir.csv')

HEADER = ['QUALITY', 'SKIP', 'SUBJECT', 'FILE-COUNT', 'BYTE-COUNT', 'SONAR-DIR']

def main():
    print('Reading from', SOURCE_DIR)
    print('Writing to', TARGET_FILE)
    with open(TARGET_FILE, 'x') as target:  # Don't overwrite a manually edited file
        writer = csv.writer(target, dialect='local')
        writer.writerow(HEADER)
        for subdir in SOURCE_DIR.glob('W?-?-?-?_*'):
            subject = subdir.name.split('_', 1)[1].replace('_', ' ')
            file_count = sum(1 for f in subdir.glob('*.xml'))
            byte_count = sum(os.stat(str(f)).st_size for f in subdir.glob('*.xml'))
            quality = 5 if file_count else 0  # To be edited manually
            skip = None if file_count else True
            writer.writerow([quality, skip, subject, file_count, byte_count, subdir])
            print('  {}'.format(subject))

if __name__ == '__main__':
    main()
