# python textgen.py couperus.plain.txt

# Train on text:
# 1. split in sentences (use list of abbreviations used in corpus)
# 2. save sentence-initial and sentence-final words separately
# 3. split the text in words, save all sequences of 2 words + 1 word (bigram model), and of 1 word + 1 word (unigram model)
# Generate new text:
# 1. each new paragraph starts with a word that occurs as begin-of-sentence in the training text
# 2. start generating sentences until the minimum paragraph length has reached
# 3. the start of a sentence is a random word based on the last two words of the previous sentence.
# 4. words are generated randomly using the previous two words in the sentence (bigram model). If those do not exist in the style dictionary, use only the previous word (unigram model).
# 5. words are generated until a sentence ending is encountered.

# the output is printed to inputfile.random[0-9]

import sys
import re
import random
from random import randint
#import numpy



textfile = sys.argv[1]
language = "dutch"
number_of_paragraphs = 8
minimum_paragraph_length = 30

outputfile = textfile+".random"+str(randint(1,100))

abbreviations_array = []
with  open("abbreviations.txt",'r') as abbrevfile:
    for line in abbrevfile:
        abbrev = line.rstrip()
        abbrev = re.sub("\.$","",abbrev)
        #print (abbrev)
        abbreviations_array.append(abbrev)


abbreviations = "("+"|".join(abbreviations_array)+")[.]"
caps = "([A-Z])"
nocaps = "([a-z])"
numbers = "([0-9])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"

if language == "dutch":
    prefixes = "(Dhr|Mevr|Dr|Drs|Mr|Ir|Ing)[.]"
    suffixes = "(BV|MA|MSc|BSc|BA)"
    starters = "(Dhr|Mevr|Dr|Drs|Mr|Ir|Ing)"
    acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
    websites = "[.](com|net|org|io|gov|nl)"

def split_into_sentences(text):
    # adapted from http://stackoverflow.com/questions/4576077/python-split-text-on-sentences
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(abbreviations,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    text = re.sub(numbers+"[.]"+numbers,"\\1<prd>\\2",text) # added by me
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\?\) +"+ nocaps,"<qbra> \\1",text) # added by me (question mark followed by closing brackets followed by nocaps
    text = re.sub("\s" + caps + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(caps + "[.]" + caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + caps + "[.]"," \\1<prd>",text)

    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = re.sub("([;:]-?[\)\(]) +","\\1<stop> ",text) # added by me (emoticons)
    text = re.sub("([\.\?!]+\)?) ","\\1<stop>",text)
    if "<stop>" not in text:
        text += "<stop>"
    text = text.replace("<prd>",".")
    text = text.replace("<qbra>","?)")
    text = re.sub('  +',' ',text)
    sents = text.split("<stop>")
    sents = sents[:-1]
    sents = [s.strip() for s in sents]
    return sents

def tokenize(t):
    #text = t.lower()
    text = t
    text = re.sub("\n"," ",text)
    #text = re.sub('[^a-zèéeêëûüùôöòóœøîïíàáâäæãåA-Z0-9- \']', "", text)
    wrds = text.split()
    return wrds

def read_text(filename):
    #Your code here
    f=open(filename,'rt')
    corpus=f.read()
    f.close()
    paragraphs = corpus.split("\n\n")

    #parlengths = []
    #for paragraph in paragraphs:
    #    words = tokenize(paragraph)
    #    parlength = len(words)
    #    parlengths.append(parlength)
    #mean_pagraph_length = numpy.mean(parlengths)
    #print ("average nr of words in paragraph:",mean_pagraph_length)
    sentences = split_into_sentences(corpus)
    return sentences

def fill_up_dict(words):
    style_dict= dict()
    print ("Fill the dictionary with bigrams and unigrams...")
    for i, word in enumerate(words[:-2]):


        if word+" "+words[i+1] in style_dict:
            #bigram model: check if the previous two words are already in the dictionary as bigram
            if not (words[i+2] == words[i+1] == words[i] and not re.match(".*[a-zA-Z]+.*",words[i])):
                # don't store sequences of non-alphabetic words or the exact same words
                style_dict[word+" "+words[i+1]].append(words[i+2])
                # then add the next word as potentially generated word for this bigram
            #else:
                #print ("Don't store: ",words[i],words[i+1],words[i+2])
        else:
            #bigram model: if the previous two words are not yet in the dictionary as bigram
            if not (words[i+2] == words[i+1] == words[i] and not re.match(".*[a-zA-Z]+.*",words[i])):
                # don't store sequences of non-alphabetic words or the exact same words
                style_dict[word+" "+words[i+1]]=[words[i+2]]
                # then store them with the next word as potentially next word for this bigram
            #else:
                #print ("Don't store: ",words[i],words[i+1],words[i+2])
        if word in style_dict:
            #unigram model: if the previous word is already in the dictionary as unigram
            style_dict[word].append(words[i+1])
            # then add the next word as potentially generated
        else:
            #unigram model: if the previous word is not yet in the dictionary as unigram
            style_dict[word]=[words[i+1]]
            # then store it with the next word as potentially generated word for this unigram

    return style_dict

# Reads text from a file, tokenizes it, and creates a style profile
# consisting of: first words, final words, unigrams and bigrams (style dict)
def make_style_dict(filename):
    sentences=read_text(filename)
    first_words = []
    last_words = dict()
    allwords = []
    print ("Split in sentences and save first and last words...")
    for sentence in sentences:
        #print (sentence)
        words = tokenize(sentence)
        for word in words:
            allwords.append(word)
        #print (sentence)
        if len(words) > 0:
            first_word = words[0]
            if re.match("^[A-Z'].*",first_word):
                first_words.append(first_word)
            if len(words) > 2:
                last_word = words[-1]
                last_words[last_word] = 1

        #words=corpus.split()

    style_dict=fill_up_dict(allwords)
    return style_dict,first_words,last_words


def generate_sentence(style_dict,first_words, last_words,first_word = ""):
    
    if not first_word:
        first_word = random.choice(first_words)
    
    sentence = []
    word = first_word
    sentence.append(word)

    while not word in last_words:

        # generate words until we encounter a word that is in the list of sentence-final words
        if len(sentence) > 1:
            # if we have context of 2 already, use bigram model
            previous_word = sentence[-2] # index -2 in the array refers to the second last word in the array
            if previous_word+" "+word in style_dict:
                # bigram model

                nextword=random.choice(style_dict[previous_word+" "+word])
##                print ("bigram model:", previous_word, word,"->",nextword)
                word = nextword
            else:
                nextword=random.choice(style_dict[word])
##                print ("unigram model:",word,"->",nextword)
                word = nextword
        else:
            # otherwise (beginning of sentence; we only have 1 word), use unigram model
            nextword=random.choice(style_dict[word])
            print ("unigram model:",word,"->",nextword)
            word = nextword
        sentence.append(word)
        #print ("sentence:", sentence)

    # generated word was a sentence-final word -> generate the first word for the next sentence
#    print("hoi")
#    print(style_dict[word])
    next_first_word = random.choice(first_words)#random.choice(style_dict[word])
    return sentence, next_first_word


def print_story(style_dict,first_words,last_words):
 #   print(style_dict)
   # print (first_words)
    paragraphs = []

    for parcount in range (number_of_paragraphs):
        #print(word)
        sentences = []
        firstword = random.choice(first_words)
        # the first word of the paragraph is a random first word

        wordcount = 1
        while wordcount < minimum_paragraph_length:
            # generate sentences as long as we haven't reached the minimum paragraph length
            sentence,next_first_word = generate_sentence(style_dict,first_words, last_words,firstword)
            # the start of a sentence is a random word based on the last two words of the previous sentence.
            sentencetext = " ".join(sentence)
            sentences.append(sentencetext)
            firstword = next_first_word
            wordcount += len(sentence)

        paragraphtext = " ".join(sentences)
        paragraphs.append(paragraphtext)

    return "\n\n".join(paragraphs)



def style_generator(fname):
    print ("Read the oeuvre and make the style dictionary...")
    style_dict,first_words,last_words=make_style_dict(fname)
    print ("Create story...")
    story=print_story(style_dict,first_words,last_words)
    story = re.sub("\n\n ","\n\n",story)
    print(story)
    out = open(outputfile,'w')
    out.write(story)
    out.close()
    #print(story)
    print ("Story printed to "+outputfile)




style_generator(textfile)


