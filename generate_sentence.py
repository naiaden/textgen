
import languagemodel
import textgenerator
import sys
import time

in_model = sys.argv[1]
out_sentence = sys.argv[2]

# load language model
lm = languagemodel.LanguageModel()
lm.load_model(in_model)

# generate sentence
tg = textgenerator.TextGenerator(lm,10)
for i in range(100):
    sentence = tg.generate_sentence()
    for word in sentence:
        print(word)
        time.sleep(0.50)
    sentence_str = ' '.join(sentence)
    sentence_str = sentence_str.replace(' .','.').replace(' !','.').replace(' ,',',').replace(' ?','?')
    print(sentence_str)

# write sentence to file
# with open(out_sentence,'w',encoding='utf-8') as file_out:
#     file_out.write(sentence)
