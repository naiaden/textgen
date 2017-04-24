import csv
import pathlib

# Standard directories

PROJECT_DIR = pathlib.Path('..').resolve()
DATA_DIR = PROJECT_DIR / 'Data'
SOURCE_DIR = PROJECT_DIR / 'Source'

CORPORA_DIR = pathlib.Path('/home/merijn/Documents/Master/Lab Rotations 1/Limerick 4/Corpora')
SONAR_DIR = CORPORA_DIR / 'SoNaR-500' / 'DATA'

# CSV dialect

class _LocalCsvDialect(csv.Dialect):
    delimiter = ';'
    doublequote = True
    escapechar = None
    lineterminator = '\n'
    quotechar = '"'
    quoting = csv.QUOTE_MINIMAL
    skipinitialspace = False
    strict = True

csv.register_dialect('local', _LocalCsvDialect)
