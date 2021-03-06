class TextGenerator:
    # Generates one sentence (list-based) until a sentence final words occurs
    def generate_sentence(self): # target = word or pos
        sentence = []
        first_word = False
        while not first_word:
            first_word = self.lm.get_first_word()
            if first_word.lower()[0] == 'q' or first_word.lower() in ['autrement','goodbye','paix','un','dieu','amboise']:
                first_word = False
        # sentence.append(self.lm.get_first_word())
        sentence.append(first_word)
        
        next_word = self.lm.get_next_word(sentence)
        while not self.lm.is_last_word(next_word):
            sentence.append(next_word)
            next_word = self.lm.get_next_word(sentence)
        
        sentence.append(next_word)
        return sentence
    
    # Generates one paragraph (list-based) until the minimum number of words is met
    def generate_paragraph(self):
        paragraph = []
        
        word_count = 0
        while word_count < self.minimum_paragraph_length:
            sentence = self.generate_sentence()
            paragraph.append(sentence)
            word_count = word_count + len(sentence)
        
        return paragraph
    
    def __init__(self, language_model, minimum_paragraph_length):
        self.lm = language_model
        self.minimum_paragraph_length = int(minimum_paragraph_length)
