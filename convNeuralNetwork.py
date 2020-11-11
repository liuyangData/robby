import json
import pickle
import numpy as np
import random
import nltk
nltk.download('punkt')
nltk.download('wordnet')

class NeuralNetwork:


    from keras.models import Sequential
    model = Sequential()
    intents = {}
    words = []
    classes = []
    ignore_words = ['?', '!']   

    documents = []    

    def __init__(self):
        pass

    def processDocument(self, file):
        self.intents = json.loads(open(file).read()) # 'intents.json'



        for intent in self.intents['intents']:
            for pattern in intent['patterns']:
                w = nltk.word_tokenize(pattern)
                self.words.extend(w)
                self.classes.append(intent['tag'])
                self.documents.append((w, intent['tag']))
                
        from nltk.stem import WordNetLemmatizer
        lemmatizer = WordNetLemmatizer()
        self.words = [lemmatizer.lemmatize(w.lower()) for w in self.words if w not in self.ignore_words]
        self.words = sorted(list(set(self.words)))
        self.classes = sorted(list(set(self.classes)))
    
    def generateTrainingData(self, documents): 
        ### Deel Learning Model 
        from nltk.stem import WordNetLemmatizer
        lemmatizer = WordNetLemmatizer()
        training = []
        output_empty = [0] * len(self.classes)
        for doc in self.documents:
            # initializing bag of words
            bag = []

            # list of tokenized words for the pattern
            pattern_words = doc[0]

            # lemmatize each word - create base word, in attempt to represent related words
            pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]

            # create our bag of words array with 1, if word match found in current pattern
            for w in self.words:
                bag.append(1) if w in pattern_words else bag.append(0)

            # output is a '0' for each tag and '1' for current tag (for each pattern)
            output_row = list(output_empty)
            output_row[self.classes.index(doc[1])] = 1

            training.append([bag, output_row])

        # shuffle our features and turn into np.array
        random.shuffle(training)
        training = np.array(training)
        return training

    def trainModel(self, training):
        
        # create train and test lists. X - patterns, Y - intents
        train_x = list(training[:,0])
        train_y = list(training[:,1])

        # Deep Learning Model: 128 by 64
        from keras.layers import Dense, Activation, Dropout
        from keras.optimizers import SGD

        self.model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(64, activation='relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(len(train_y[0]), activation='softmax'))

        # Compile model. Stochastic gradient descent with Nesterov accelerated gradient
        sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        self.model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

        #fitting and saving the model
        hist = self.model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
        self.model.save('chatbot_model.h5', hist)


### Build Chatbot 
    def loadModel(self, hist): # chatbot_model.h5
        from keras.models import load_model
        self.model = load_model(hist)


    def clean_up_sentence(self, sentence):
        from nltk.stem import WordNetLemmatizer
        lemmatizer = WordNetLemmatizer()
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
        return sentence_words

    # return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

    def bow(self, sentence, words):
        # tokenize the pattern
        sentence_words = self.clean_up_sentence(sentence)
        
        # bag of words - matrix of N words, vocabulary matrix
        bag = [0]*len(words)
        for s in sentence_words:
            for i,w in enumerate(words):
                if w == s:
                    # assign 1 if current word is in the vocabulary position
                    bag[i] = 1
        return(np.array(bag))

    def predict_class(self, sentence, model):
        # filter out predictions below a threshold
        p = self.bow(sentence, self.words)
        res = self.model.predict(np.array([p]))[0]
        ERROR_THRESHOLD = 0.25
        results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
        
        # sort by strength of probability
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({"intent": self.classes[r[0]], "probability": str(r[1])})
        return return_list

    def getResponse(self, ints, intents_json):
        tag = ints[0]['intent']
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if(i['tag']== tag):
                result = random.choice(i['responses'])
                break
        return result

    def chatbot_response(self, msg):
        ints = self.predict_class(msg, self.model)
        res = self.getResponse(ints, self.intents)
        return res

