# API

The server uses a RESTful API, with GET and PUT requests.

## Sentences

* ```/sentences``` shows all sentences used in all stories (GET)
  ```
  {"data": [{"sentence_id": 1, "sentence": "December in Londen, een koude mist."}, {"sentence_id": 2, "sentence": "Een wit waas om White-Rose, in de achterkamer een groot vuur."}
  ```
* ```/sentence/<sentence_id>``` shows the sentence with that id (GET)
 ```
 {"data": [{"sentence_id": 2, "sentence": "Een wit waas om White-Rose, in de achterkamer een groot vuur."}]}
 ```
* ```/addsentence/<story_id>``` adds a sentence to a story (PUT), i.e. ```curl -X PUT http://localhost:5003/addsentence/3 -d data="Het sneeuwde met groote vlokken."```
  ```
  {"status": "sentence added"}
  ```

## Stories

* ```/stories``` shows all stories with their sentences and their positions (GET)
 ```
 {"data": [{"story_id": 1, "sentence_id": 6, "position": 1}, {"story_id": 1, "sentence_id": 7, "position": 2}, {"story_id": 2, "sentence_id": 3, "position": 1}, {"story_id": 1, "sentence_id": 8, "position": 3}, {"story_id": 2, "sentence_id": 5, "position": 3}, {"story_id": 2, "sentence_id": 4, "position": 2}, {"story_id": 3, "sentence_id": 11, "position": 1}, {"story_id": 17, "sentence_id": 14, "position": 1}]}
 ```
* ```/story/<story_id>``` shows the story with its sentences and positions (GET)
 ```
 {"data": [{"story_id": 2, "sentence_id": 3, "position": 1}, {"story_id": 2, "sentence_id": 5, "position": 3}, {"story_id": 2, "sentence_id": 4, "position": 2}]}
```
* ```/createstory<author_id>``` creates a new (empty) story for an ```author_id``` (GET)

## Author

* ```/authors``` shows a list of all available authors (GET)
```
{"data": [{"author_id": 1, "name": "Louis Couperus"}, {"author_id": 2, "name": "Annie M.G. Schmidt"}]}
```

## Votes

* ```/votes``` shows all votes that have been cast (GET)
```
{"data": [{"sentence_id": 12, "vote_id": 4}, {"sentence_id": 13, "vote_id": 5}, {"sentence_id": 14, "vote_id": 6}]}
```
* ```/vote/<suggestion_id>``` cast vote for suggestion, which turns the suggestion into a sentence, and is added to the story (PUT)
```
{
  "vote_id": 4
}
```
* ```/vote/<suggestion_id>``` shows the vote info

## Suggestions

* ```/suggestion/<story_id>``` get a list of suggestions on how to continue with the story (GET)
```
[
  {
    "sentence": "Stt ...", 
    "suggestion_id": 20
  }, 
  {
    "sentence": "Oneindig verstand , zegt hij in een heftige sc\u00e8ne van opstand uitbarstte , en vloekte ...", 
    "suggestion_id": 21
  }, 
  {
    "sentence": "Diego een bizondere pozitie hebben bekleed : edelman en bemiddeld kreeg hij er zelfs een formeele strijd tusschen hem en haar zelf , en 's nachts , 's morgens .", 
    "suggestion_id": 22
  }, 
  {
    "sentence": "Vier-en-twintig lictoren , de omkranste ro\u00eabundels-en-bijlen torsend , omstuwen de statie-kar , aan beide zijden verdeelde en tegen de regenten , en bijgevolg in voortdurende wording en herwording is .", 
    "suggestion_id": 23
  }, 
  {
    "sentence": "W\u00ecl u nu wat eten ....", 
    "suggestion_id": 24
  }, 
  {
    "sentence": "Blauw Paradijs , wat waren het mooie , het edele , opofferende van hare lichtzinnige daad .", 
    "suggestion_id": 25
  }
]
```


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
