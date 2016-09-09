
import ucto
import frog

def tokenize_txt(infile, configfile):
    """
    Function to retrieve tokenized sentences from a file, used as input for training a language model. Punctuation is included in the output.

    Input:
    - infile: plain txt file in utf-8 encoding
    - configfile: file used to configure ucto. When using LaMachine all configfiles can be found in 'etc/ucto/'

    Output:
    list of lists, representing sentences and words/punctuation in a sentence.
    """
    # initialize output
    sentences = []
    sentence = []
 
    # open file and extract lines
    with open(infile, 'r', encoding = 'utf-8') as fileread:
        lines = fileread.readlines()

    # initialize tokenizer
    tokenizer = ucto.Tokenizer(configfile)

    # for each line
    for line in lines:
        # tokenize    
        tokenizer.process(line)
        # add each token to the sentence...
        for token in tokenizer:
            sentence.append(token.text)
            # ...until the sentence ends
            if token.isendofsentence():
                sentences.append(sentence)
                # initialize a new sentence
                sentence = []

    if len(sentence) > 0:
        sentences.append(sentence)

    return sentences

def frog_txt(infile):
    """
    Function to retrieve tokenized and pos-tagged sentences from a file, used as input for training a language model. Punctuation is included in the output.

    Input:
    - infile: plain txt file in utf-8 encoding

    Output:
    list of lists, representing sentences and words/punctuation + postags in a sentence.
    """
    # initialize output
    sentences = []
    sentence = []
 
    # open file and extract lines
    with open(infile, 'r', encoding = 'utf-8') as fileread:
        lines = fileread.readlines()

    # initialize frogger
    fo = frog.FrogOptions(ner=False, chunking=False, mwu=False, lemma=False, morph=False, daringmorph=False)
    frogger = frog.Frog(fo)

    numlines = len(lines)
    if numlines > 1000:
        reports = range(0, numlines, 1000)
    elif numlines > 100:
        reports = range(0, numlines, 10)
    else:
        reports = range(numlines)
    # for each line
    for i, line in enumerate(lines):
        if i in reports:
            print(i, 'of', numlines, 'lines frogged.')
        # frog    
        frogged = frogger.process(line)
        # add each token to the sentence...
        for token in frogged:
            sentence.append({'word':token['text'], 'pos':token['pos']})
            # ...until the sentence ends
            if 'eos' in token:
                sentences.append(sentence)
                # initialize a new sentence
                sentence = []

    # scrape last bits of info
    if len(sentence) > 0:
        sentences.append(sentence)

    return sentences
