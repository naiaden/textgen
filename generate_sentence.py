
import languagemodel
import textgenerator
import sys

in_model = sys.argv[1]
out_sentence = sys.argv[2]

# load language model
lm = languagemodel.LanguageModel()
lm.load_model(in_model)

# generate sentence
tg = textgenerator.TextGenerator(lm,10)
sentence = ' '.join(tg.generate_sentence())

# write sentence to file
with open(out_sentence,'w',encoding='utf-8') as file_out:
    file_out.write(sentence)
