
import textgenerator
import languagemodel
import sentence_semantics
import json
import sys
import random

in_lm = sys.argv[1]
in_wtv = sys.argv[2]
outfile = sys.argv[3]

print('reading in language model')
lm = languagemodel.LanguageModel()
lm.load_model(in_lm)
tg = textgenerator.TextGenerator(lm,10)

print('generating candidates')
sensem = sentence_semantics.SentenceSemantics()
sensem.load_model(in_wtv)

print('writing story')
target = tg.generate_sentence()
with open(outfile,'w',encoding='utf-8') as w_out:
    w_out.write('start : ' + ' '.join(target) + '\n')
    for i in range(50):
        print(i,'of',50)
        sources = [tg.generate_sentence() for x in range(1000)]
        candidates = sensem.return_sentence_candidates(target,sources,8)
        pick = random.choice([x[0] for x in candidates])
        w_out.write(str(i) + ' : ' + ' '.join(pick) + '\n')
        target = pick
