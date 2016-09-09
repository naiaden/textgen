#!/usr/bin/python3

import string

class LanguageModel:
    'Combines the features into a language model'
    first_words = {}
    last_words = {}
    unigrams = {}
    bigrams = {}
    
    def last_word_feature(self, sentence):
        if(sentence and sentence[-1][-1] in string.punctuation):
            self.last_words[sentence[-1]] = self.last_words.get(sentence[-1], 1)
    
    def start_word_feature(self, sentence):
        if(sentence and sentence[0][0].isupper()):
            self.first_words[sentence[0]] = self.first_words.get(sentence[0], 1)
    
    def unigram_feature(self, sentence):
        if(sentence):
            for token in sentence:
                self.unigrams[token] = self.unigrams.get(token, 1)
    
    def bigram_feature(self, sentence):
        if(sentence):
            for bigram in [' '.join(sentence[i:i+2]) for i in range(len(sentence)-1)]:
                self.bigrams[bigram] = self.bigrams.get(bigram, 1)
    
    def generate_features(self, sentences):
        for sentence in sentences:
            self.start_word_feature(sentence)
            self.last_word_feature(sentence)
            self.unigram_feature(sentence)
            self.bigram_feature(sentence)
    
    def print_features(self):
        print("First words:")
        print(self.first_words)
        
        print("Last words:")
        print(self.last_words)
        
        print("Unigrams:")
        print(self.unigrams)
        
        print("Bigrams:")
        print(self.bigrams)
    
    def __init__(self, sentences):
        print("number of sentences: " + str(len(sentences)))
        self.generate_features(sentences)

lm = LanguageModel([['Dit', 'is', 'een', 'korte', 'zin'], ['waar', 'er', 'meer', 'van', 'zijn.']])
lm.print_features()
