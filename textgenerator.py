class TextGenerator:
    minimum_paragraph_length = 30
    
    def generate_sentence(self):
        sentence = []
        sentence.append(self.lm.get_first_word())
        
        next_word = self.lm.get_next_word(sentence)
        while not self.lm.is_last_word(next_word):
            sentence.append(next_word)
            next_word = self.lm.get_next_word(sentence)
        
        sentence.append(next_word)
        return sentence
    
    def generate_paragraph(self):
        paragraph = []
        
        word_count = 1
        while word_count < self.minimum_paragraph_length:
            sentence = self.generate_sentence()
            paragraph.append(sentence)
            word_count += len(sentence)
        
        return paragraph

    def __init__(self, language_model):
        self.lm = language_model
        print(self.generate_paragraph())