import random

class MarkovChain:

    corpus = []
    transitional_1gram = {}
    transitional_2gram = {}
    transitional_3gram = {}

    def __init__(self):
        pass

    def loadCorpus(self, file):
        import json
        with open(file, 'r') as f:
            for sentence in json.load(f):
                for word in sentence.split():
                    self.corpus.append(word)
                self.corpus.append(".")

    def generateTransitionalMatrix(self):

        # 1-gram transitional Matrix
        uniqueWords = set(self.corpus)   
        for word in uniqueWords:
            ind = self.get_index_positions(self.corpus, word)
            nextWords = [] 
            for i in ind:
                try:
                    nextWords.append(self.corpus[i+1])
                except:
                    pass
            self.transitional_1gram[word] = nextWords

        ### 2-gram Markov Chain
        for word in uniqueWords:
            ind = self.get_index_positions(self.corpus, word)
            for i in ind:
                try:
                    secondWord = self.corpus[i+1]
                    phrase = word + ' ' + secondWord
                    if '.' not in phrase:
                        try:
                            thirdWord = self.corpus[i+2]
                            if phrase in self.transitional_2gram.keys():
                                self.transitional_2gram[phrase].append(thirdWord)
                            else:
                                self.transitional_2gram[phrase] = [thirdWord]
                        except:
                            pass
                except:
                    pass
            
        ### 3-gram Markov Chain 
        for word in uniqueWords:
            ind = self.get_index_positions(self.corpus, word)
            for i in ind:
                try:
                    secondWord = self.corpus[i+1]
                    try:
                        thirdWord = self.corpus[i+2]
                        phrase = word + ' ' + secondWord + ' ' + thirdWord
                        if '.' not in phrase:
                            try:
                                fourthWord = self.corpus[i+3]
                                if phrase in self.transitional_3gram.keys():
                                    self.transitional_3gram[phrase].append(fourthWord)
                                else:
                                    self.transitional_3gram[phrase] = [fourthWord]
                            except:
                                pass
                    except:
                        pass
                except:
                    pass


    def get_index_positions(self, list_of_elems, element):

        ''' Returns the indexes of all occurrences of give element in
        the list- listOfElements '''
        index_pos_list = []
        index_pos = 0
        while True:
            try:
                index_pos = list_of_elems.index(element, index_pos)
                index_pos_list.append(index_pos)
                index_pos += 1
            except ValueError as e:
                break
        return index_pos_list

    def generate_1gram(self, word):    
        sentence = word
        while word != ".":
            word = random.choice(self.transitional_1gram[word])
            try:
                word = random.choice[self.transitional_2gram[sentence]]
            except:
                pass 
            try:
                word = random.choice[self.transitional_3gram[sentence]]
            except:
                pass
            sentence = sentence + " " + word 
        return sentence

    def generate_2gram(self, phrase):
        sentence = phrase
        word = ''
        while word != '.':
            try:
                word = random.choice(self.transitional_2gram[phrase])
                phrase = phrase.split()[1] + ' ' + word
                sentence = sentence + ' ' + word
            except:
                word = '.'
        return sentence

    def generate_3gram(self, phrase):
        sentence = phrase
        word = ''
        while word != '.':
            try:
                word = random.choice(self.transitional_3gram[phrase])
                phrase = phrase.split()[1] + ' ' + phrase.split()[2] + ' ' + word
                sentence = sentence + ' ' + word
            except: 
                word = '.'
        return sentence

    def generate_sentence(self, text):

        if " " not in text:
            return self.generate_1gram(text)

        text = text.lower()
        words = text.split()
        if len(words) == 3:
            return self.generate_3gram(text)
        elif len(words) == 2:
            return self.generate_2gram(text)
        