
import ucto

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
        tokenized_line = tokenizer.process(line)
        # add each token to the sentence...
        for token in tokenized_line:
            sentence.append(token.text)
            # ...until the sentence ends
            if token.isendofsentence():
                sentences.append(sentence)
                # initialize a new sentence
                sentence = []

    if len(sentence) > 0:
        sentences.append(sentence)

    return sentences
