
#from gensim.models import Word2Vec
import gensim


class SentenceSemantics:

    def __init__(self):
        self.model = False

    def train_model(self,sentences):
        self.model = Word2Vec(sentences,min_count=5,iter=1,workers=8)

    def save_model(self,outfile):
        self.model.save_word2vec_format(outfile,binary=True)

    def load_model(self,modelfile):
        self.model = gensim.models.KeyedVectors.load_word2vec_format(modelfile,binary=True)

    def remove_stopwords_sentence(self,sentence,stopwords):
        clean_sentence = list(set(sentence) - stopwords)
        return clean_sentence

    def remove_stopwords_sentences(self,sentences,stopwords):
        clean_sentences = []
        for sentence in sentences:
            clean_sentence = self.remove_stopwords_sentence(sentence,stopwords)
            clean_sentences.append(clean_sentence)
        return clean_sentences

    def sentence_similarity(self,sentence1,sentence2):
        sen1_match = [word for word in sentence1 if word in self.model.vocab]
        sen2_match = [word for word in sentence2 if word in self.model.vocab]
        if len(sen1_match)>0 and len(sen2_match)>0:
            sim = self.model.n_similarity(sen1_match, sen2_match)
        else:
            sim = 0
        return sim
        
        #return self.model.n_similarity([word for word in sentence1 if word in self.model.vocab], [word for word in sentence2 if word in self.model.vocab])

    def rank_sentences_similarity(self,target_sentence,source_sentences):
        sentence_similarity = []
        for source_sentence in source_sentences:
            sensim = self.sentence_similarity(target_sentence,source_sentence)
            sentence_similarity.append((source_sentence,sensim))
        sentence_similarity_sorted = sorted(sentence_similarity,key=lambda k : k[1],reverse=True)
        return sentence_similarity_sorted

    def return_sentence_candidates(self,target_sentence,source_sentences,candidate_ranks=[1,10,50]):
        sorted_sentences = self.rank_sentences_similarity(target_sentence,source_sentences)
        return [sorted_sentences[i] for i in candidate_ranks]
