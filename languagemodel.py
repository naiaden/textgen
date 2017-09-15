#!/usr/bin/python3

import string # for the bigrams
import random # for get_first_word
import json   # save and load target

class LanguageModel:
    
    def get_first_word(self):
        return random.choice(list(self.first_words.keys()))
    
    # Get word, with a priori knowledge
    def get_zerogram(self, target=None):
        if target is None:
            target = self.ngrams
        return random.choice(list(target.keys()))
    
    # Get word, based on the unigram context
    def get_unigram(self, word, target=None):
        if target is None:
            target = self.ngrams
        
        if word in target:
            followers = target[word]['followers']
            if followers:
                return random.choice(list(followers.keys()))
        return self.get_zerogram()
    
    # Get word, based on the bigram context
    def get_bigram(self, w1, w2, target=None):
        if target is None:
            target = self.ngrams
        
        if w1 in target:
            if w2 in target[w1]['followers']:
                followers = target[w1]['followers'][w2]['followers']
                if followers:
                    return random.choice(list(followers.keys()))
        return self.get_unigram(w2)
    
    # Get word, based on the trigram context
    def get_trigram(self, w1, w2, w3, target=None):
        if target is None:
            target = self.ngrams
        
        if w1 in target:
            if w2 in target[w1]['followers']:
                if w3 in target[w1]['followers'][w2]['followers']:
                    followers = target[w1]['followers'][w2]['followers'][w3]['followers']
                    if followers:
                        return random.choice(list(followers.keys()))
        return self.get_unigram(w3)
    
    # Get word, based on a sentence
    def get_next_word(self, sentence):
        if len(sentence) / len(list(set(sentence))) > 10: # gotten in some endless loop
            return self.get_first_word()
        if not sentence:
            return self.get_first_word()
        elif len(sentence) == 1:
            return self.get_unigram(sentence[0])
        elif len(sentence) == 2:
            return self.get_bigram(sentence[-2], sentence[-1])
        else:
            return self.get_trigram(sentence[-3], sentence[-2], sentence[-1])

    def is_last_word(self, word):
        if word in self.last_words:
            return True
        return False
    
    # Store all the sentence final words with punctuation
    def last_word_feature(self, sentence):
        if(sentence and sentence[-1]['word'][-1] in ['.', '?', '!']):#string.punctuation):
            self.last_words[sentence[-1]['word']] = self.last_words.get(sentence[-1]['word'], 1)
    
    # Store all the sentence initial words with capitals
    def start_word_feature(self, sentence):
        if(sentence and sentence[0]['word'][0].isupper()):
            self.first_words[sentence[0]['word']] = self.first_words.get(sentence[0]['word'], 1)
    
    # Store all unigrams (token unigrams if code is 'word', pos unigrams if code is 'pos'), and their frequency
    def unigram_feature(self, sentence, code, target): # code = 'word', 'pos', target = ngrams, pos_ngrams
        if(sentence):
            for token in sentence:
                w1 = token[code]
                if w1 in target:
                    target[w1]['count'] = 1 + target[w1]['count']
                else:
                    target[w1] = {}
                    target[w1]['count'] = 1
                    target[w1]['followers'] = {}
    
    # Store all bigrams (token unigrams if code is 'word', pos unigrams if code is 'pos'), in a trie structure
    def bigram_feature(self, sentence, code, target): # code = 'word', 'pos', target = ngrams, pos_ngrams
        if(sentence):
            for bigram in [sentence[i:i+2] for i in range(len(sentence)-1)]:
                w1 = bigram[0][code]
                w2 = bigram[1][code]
                if w2 in target[w1]['followers']:
                    target[w1]['followers'][w2]['count'] = 1 + target[w1]['followers'][w2]['count']
                else:
                    target[w1]['followers'][w2] = {}
                    target[w1]['followers'][w2]['count'] = 1
                    target[w1]['followers'][w2]['followers'] = {}
    
    # Store all trigrams (token unigrams if code is 'word', pos unigrams if code is 'pos'), in a trie structure
    def trigram_feature(self, sentence, code, target): # code = 'word', 'pos', target = ngrams, pos_ngrams
        if(sentence):
            for trigram in [sentence[i:i+3] for i in range(len(sentence)-2)]:
                w1 = trigram[0][code]
                w2 = trigram[1][code]
                w3 = trigram[2][code]
                if w3 in target[w1]['followers'][w2]['followers']:
                    target[w1]['followers'][w2]['followers'][w3]['count'] = 1 + target[w1]['followers'][w2]['followers'][w3]['count']
                else:
                    target[w1]['followers'][w2]['followers'][w3] = {}
                    target[w1]['followers'][w2]['followers'][w3]['count'] = 1
                    target[w1]['followers'][w2]['followers'][w3]['followers'] = {}

    # Store all trigrams (token unigrams if code is 'word', pos unigrams if code is 'pos'), in a trie structure
    def fourgram_feature(self, sentence, code, target): # code = 'word', 'pos', target = ngrams, pos_ngrams
        if(sentence):
            for fourgram in [sentence[i:i+4] for i in range(len(sentence)-3)]:
                w1 = fourgram[0][code]
                w2 = fourgram[1][code]
                w3 = fourgram[2][code]
                w4 = fourgram[3][code]
                if w4 in target[w1]['followers'][w2]['followers'][w3]['followers']:
                    target[w1]['followers'][w2]['followers'][w3]['followers'][w4]['count'] = 1 + target[w1]['followers'][w2]['followers'][w3]['followers'][w4]['count']
                else:
                    target[w1]['followers'][w2]['followers'][w3]['followers'][w4] = {}
                    target[w1]['followers'][w2]['followers'][w3]['followers'][w4]['count'] = 1
    
    # Normally this would be according to some fancy design pattern with registration. But today it isn't
    def generate_features(self, sentences):
        for sentence in sentences:
            self.start_word_feature(sentence)
            self.last_word_feature(sentence)
            self.unigram_feature(sentence, 'word', self.ngrams)
            self.unigram_feature(sentence, 'pos', self.pos_ngrams)
            self.bigram_feature(sentence, 'word', self.ngrams)
            self.bigram_feature(sentence, 'pos', self.pos_ngrams)
            self.trigram_feature(sentence, 'word', self.ngrams)
            self.trigram_feature(sentence, 'pos', self.pos_ngrams)
            self.fourgram_feature(sentence, 'word', self.ngrams)
            self.fourgram_feature(sentence, 'pos', self.pos_ngrams)
    
    def print_features(self):
        print("First words:")
        print(self.first_words)
        
        print("Last words:")
        print(self.last_words)
        
        print("ngrams:")
        print(self.ngrams)
        
        print("pos_ngrams:")
        print(self.pos_ngrams)

    def load_model(self, model_saved):
        # read in target
        with open(model_saved, 'r', encoding = 'utf-8') as file_in:
            model = json.load(file_in)
        self.first_words = model[0]
        self.last_words = model[1]
        self.ngrams = model[2]
        self.pos_ngrams = model[3]

    def save_model(self, outfile):
        # write target to file
        with open(outfile, 'w', encoding = 'utf-8') as file_out:
            json.dump([self.first_words,self.last_words,self.ngrams,self.pos_ngrams], file_out)

    def train_model(self, sentences):
        #print("number of sentences: " + str(len(sentences)))
        self.generate_features(sentences)
        #print(self.ngrams.keys())

    def __init__(self):
        'Combines the features into a language model'
        self.first_words = {}
        self.last_words = {}
        self.ngrams = {} # Dict(count:int, followers:[])
        self.pos_ngrams = {} # Dict(count:int, followers:[]
