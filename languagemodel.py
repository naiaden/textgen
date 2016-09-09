#!/usr/bin/python3



class LanguageModel:
    'Combines the features into a language model'
    first_words = {}
    last_words = {}

    def start_word_feature(self, sentence):
        if(sentence and sentence[0][0].isupper()):
            first_words[sentence[0]] = first_words.get(sentence[0], 1)

    def __init__(self, sentences):
        print("number of sentences: " + str(len(sentences)))

print("Nice")
