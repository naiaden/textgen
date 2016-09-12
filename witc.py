# Writers in the Cloud
#
#
import configparser
import json
from languagemodel import LanguageModel
from textgenerator import TextGenerator

config = configparser.ConfigParser()
config.read('witc.ini')

cache_file = config['INPUT']['CacheFile']
minimum_paragraph_length = int(config['OUTPUT'].get('MinimumParagraphLength', 30))

if cache_file:
    print("+ Reading cache file")
    with open(cache_file) as data_file:
        data = json.load(data_file)

print("+ Creating language model")
lm = LanguageModel(data)

print("+ Generating text")
tg = TextGenerator(lm, minimum_paragraph_length)
print(tg.generate_paragraph())

