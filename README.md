# API

The server uses a RESTful API, with GET and PUT requests.

## Sentences

/sentences shows all sentences used in all stories (GET)
/sentence/<sentence_id> shows the sentence with that id (GET)
/addsentence/<story_id> adds a sentence to a story (PUT), i.e. curl -X PUT http://localhost:5003/addsentence/3 -d data="Het sneeuwde met groote vlokken."

## Stories

/stories shows all stories with their sentences and their positions (GET)
/story/<story_id> shows the story with its sentences and positions (GET)
/createstory<author_id> creates a new (empty) story for an author (GET)

## Author

/authors shows a list of all available authors (GET)

## Votes

/votes shows all votes that have been cast (GET)
/vote/<suggestion_id> cast vote for suggestion, which turns the suggestion into a sentence, and is added to the story (GET)

## Suggestions

/suggestion/<story_id> get a list of suggestions on how to continue with the story (GET)


# textgen
Script for generating text in the style of the oeuvre that is added as argument (in plain text).

Steps that the script takes:

A. Train on text:
 1. split in sentences (use list of abbreviations used in corpus)
 2. save sentence-initial and sentence-final words separately
 3. split the text in words, save all sequences of 2 words + 1 word (bigram model), and of 1 word + 1 word (unigram model)

B. Generate new text:
 1. each new paragraph starts with a word that occurs as begin-of-sentence in the training text
 2. start generating sentences until the minimum paragraph length has reached
 3. the start of a sentence is a random word based on the last two words of the previous sentence.
 4. words are generated randomly using the previous two words in the sentence (bigram model). If those do not exist in the style dictionary, use only the previous word (unigram model).
 5. words are generated until a sentence ending is encountered.

Minimal paragraph length and number of paragraphs are user-defined in the script (TODO: redefine as arguments)

The output is printed to inputfile.random[0-9]+


# Usage

Pre-training models:

python generate_features.py /vol/bigdata2/datasets2/WritersintheCloud/kellendonktxt/kellendonk.feats.json /vol/customopt/lamachine/share/frog/nld/frog.cfg /vol/bigdata2/datasets2/WritersintheCloud/kellendonktxt/Verzameld\ werk\ -\ Frans\ Kellendonk.txt

python train_lm.py /vol/bigdata2/datasets2/WritersintheCloud/kellendonktxt/kellendonk.feats.json /vol/bigdata2/datasets2/WritersintheCloud/kellendonktxt/kellendonk.lm.json

Online text generation:
