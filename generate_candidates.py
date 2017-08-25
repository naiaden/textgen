
import sys

import languagemodel
import textgenerator
import sentence_semantics

in_lm = sys.argv[1] # file storing the language model
in_w2v = sys.argv[2] # file storing the word-to-vec model
in_target = sys.argv[3] # file storing the target sentence
#in_stopwords = sys.argv[4] # file with stopwords
out_candidates = sys.argv[4] # file to write the output candidates to

# load language model
lm = languagemodel.LanguageModel()
lm.load_model(in_lm)
tg = textgenerator.TextGenerator(lm,10)

# load w2v model
sensem = sentence_semantics.SentenceSemantics()
sensem.load_model(in_w2v)

# read in target sentence
with open(in_target,'r',encoding='utf-8') as target_in:
    target_sentence = target_in.read().strip().split()

# # read in stopwords
# with open(in_stopwords, 'r', encoding='utf-8') as sw_in:
#     stopwords = set(sw_in.read().strip().split('\n'))

# generate candidates
sources = [tg.generate_sentence() for x in range(10000)] # the candidates are drawn from a pool of 1000 randomly generated sentences
#target_sentence_clean = sensem.remove_stopwords_sentence(target_sentence,stopwords)
#sources_clean = sensem.remove_stopwords_sentences(sources,stopwords)

candidates = sensem.return_sentence_candidates(target_sentence,sources)
print('TARGET:',' '.join(target_sentence))
print('CANDIDATES:','\n'.join([', '.join([' '.join(c[0]),str(c[1])]) for c in candidates]))

with open(out_candidates,'w',encoding='utf-8') as file_out:
    file_out.write('\n'.join([' '.join(c[0]) for c in candidates]))
