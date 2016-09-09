#!/usr/bin/python3

import string

class LanguageModel:
    'Combines the features into a language model'
    first_words = {}
    last_words = {}
    
    def last_word_feature(self, sentence):
        if(sentence and sentence[-1][-1] in punctuation):
            last_words[sentence[-1]] = last_words.get(sentence[-1], 1)
    
    def start_word_feature(self, sentence):
        if(sentence and sentence[0][0].isupper()):
            first_words[sentence[0]] = first_words.get(sentence[0], 1)
    
    def unigram_feature(self, sentence):
        if(sentence):
            for token in sentence:
                unigrams[token] = unigrams.get(token, 1)
    
    def __init__(self, sentences):
        print("number of sentences: " + str(len(sentences)))

print("Nice")
