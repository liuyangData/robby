import string
import json
import random 

# Main Parent Chatbot Class
class Chatbot:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"{self.name} is a chatbot"
    
    # Main Actions
    def speak(self, words):
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)
        engine.say(words)
        engine.runAndWait()

    def hearMic(self):
        import speech_recognition as sr
        r = sr.Recognizer()
        flag = True    
        while flag:
            with sr.Microphone() as source:
                print("Say something!")
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
            try:
                inp = r.recognize_google(audio)
                flag = False
            except sr.UnknownValueError:
                print("Robby could not understand audio")
            except sr.RequestError as e:
                print("Request error; {0}".format(e))
        return inp


# Child of Chatbot Class
class IR_Bot(Chatbot):

    dictionary = {}
    def loadDictJson(self, dictionary):
        self.dictionary.update(json.load(open(dictionary, 'r')))
    
    def loadDictionary(self, dictionary):
        self.dictionary= dictionary

    def reply(self, text):
        keys = self.dictionary.keys() 
        text = text.translate(str.maketrans("","",string.punctuation)).lower().split()
        
        for key in keys:
            for word in text:
                if word == key:
                    response = word

        try:
            reply = self.dictionary[response]
        except:
            reply = 'Sorry I could not understand, could you rephrase your sentence? To assist you better, please type one quesiton at a time, or use any of keywords here: 1) promotion 2) vouchers 3) refund 4) parcel'
        return reply


# Child of Chatbot Class 
class ML_Bot(Chatbot):
    import pandas as pd
    from chatterbot import ChatBot
    from chatterbot.trainers import ListTrainer
    from chatterbot.trainers import ChatterBotCorpusTrainer

    bot = ChatBot(name='ML_Bot',  
            logic_adapters=['chatterbot.logic.BestMatch'])
    trainer = ListTrainer(bot)
    corpus_trainer = ChatterBotCorpusTrainer(bot)

    def trainCorpus(self):
        self.corpus_trainer.train('chatterbot.corpus.english')

    def trainJSON(self, file):
        self.trainer.train(json.load(open(file, 'r')))
    
    def reply(self, text):
        return self.bot.get_response(text)

# Hybrid Chatbot Model: Child of Chatbot Class

class Robby(Chatbot):

    import pandas as pd

    from convNeuralNetwork import NeuralNetwork
    nn = NeuralNetwork()

    from mindPalace import MindPalace
    mind = MindPalace()
    #mind.loadMindPalace('mindPalace.json')

    from markovChain import MarkovChain
    markov = MarkovChain()

    from chatterbot import ChatBot
    from chatterbot.trainers import ListTrainer
    model = ChatBot(name='rob', logic_adapters=['chatterbot.logic.BestMatch'])
    trainer = ListTrainer(model)
    convAIMemory = ["Hello"]

    echoRepeatMemory = ["Hello"]
    
    def trainJSON(self, file):
        with open(file, 'r') as f:
            self.trainer.train(json.load(f))
    
    # Information Retrieval
    def reply(self, statement):

        # Structured Replies
        if self.containsAny(self.adjectives, statement.lower()):
            word = self.identify(self.adjectives, statement.lower())
            return f"What is so {word} about it?"

    # Echo Repeat System
    def loadEchoRepeat(self):
        with open('echoRepeat.json', 'r') as fp:
            self.echoRepeatMemory = json.load(fp)

    def echoRepeat(self, statement):
        if (statement in self.echoRepeatMemory):
            allIndices = [i for i, x in enumerate(self.echoRepeatMemory) if x == statement]
            reply = self.echoRepeatMemory[random.choice(allIndices)+1]
            self.echoRepeatMemory.append(statement)
            self.echoRepeatMemory.append(reply)
        else:
            reply = statement
            self.echoRepeatMemory.append(statement)
        return reply
    
    def saveEchoRepeat(self):
        json.dump(self.echoRepeatMemory, open('echoRepeat.json', 'w'))

    # ConvAI
    def loadConvAI(self):
        with open('convAI.json', 'r') as fp:
            self.convAIMemory = json.load(fp)

    def convAI(self, statement):
        reply = None
        if (statement in self.convAIMemory):
            allIndices = [i for i, x in enumerate(self.convAIMemory) if x == statement]
            reply = self.convAIMemory[random.choice(allIndices)+1]
        return reply


    # Markov Sentence Generation
    def markovLoad(self, file): # 'convAI.json'
        self.markov.loadCorpus(file)

    def mutter(self):
        topics = ["i am a", "i like to", 'i think that']
        return self.markov.generate_sentence(random.choice(topics))


    # Neural Network
    def loadNeuralNetwork(self, file, load=False):
        self.nn.processDocument(file)
        if load:
            self.nn.loadModel('chatbot_model.h5')
        else:
            self.nn.trainModel(self.nn.generateTrainingData(self.nn.documents))
    
    def neuralNetResponse(self, text):     
        return self.nn.chatbot_response(text)

    # Mind Palace 
    
    def initiateTopic(self):
        return self.mind.askHobby()

    # Instance Methods
    def containsAll(self, words, statement):
        flag = True
        for word in words:
            if word not in statement:
                flag = False 
        return flag

    def containsAny(self, words, statement):
        flag = False
        for word in words:
            if word in statement:
                flag = True 
        return flag

    def identify(self, ls1, lst2):
        word = ''
        for w in ls1:
            if w in lst2:
                word = w
        return word
 
