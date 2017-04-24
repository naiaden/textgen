from itertools import filterfalse

class NormaliserFactory:
	
	def __init__(self, data, normalisers):
		for normaliser in normalisers.split(","):
			if normaliser == "Frog":
				print("+ Normalising frogged data")
				FrogNormaliser(data)
			else:
				print("x " + normaliser + " is not implemented")

class FrogNormaliser:
    """
        We append the punctuation to their word.
    """
    def __init__(self, data):
        sentence = data[0]
        for sentence in data:
            for i,word in enumerate(sentence):
                if i > 0:
                    if word['pos'] == "LET()":
                        sentence[i-1]['word'] = sentence[i-1]['word'] + word['word']
            sentence[:] = filterfalse(lambda x: x['pos'] == "LET()", sentence)
