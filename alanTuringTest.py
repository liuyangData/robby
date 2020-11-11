from chatbot import Chatbot
import json


print("Choose an agent: IR, ML, RB")
agent = input()


### Information Retrieval System


if agent == 'IR':

    print("Meet the IR Bot. Say something")

    from chatbot import IR_Bot

    ir = IR_Bot('ir')
    ir.loadDictJson('irDictionary.json')

    userResponse = input()
    while 'quit' not in userResponse:
        print(ir.reply(userResponse))
        userResponse = input()


# Machine Learning Bot

if agent == 'ML':

    print("Meet the ML Bot. Say something:")

    from chatbot import ML_Bot

    ml = ML_Bot("ML")
    ml.trainJSON('convAI.json')

    userResponse = input()
    while 'quit' not in userResponse:
        print(ml.reply(userResponse))
        userResponse = input()


# Hybrid Chatbot: Robby

if agent == 'RB':
    
    print("Meet Robby. Say something:")
    res = input()

    while res != 'bye':
        print(model.get_response(res))
        res = input()





from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import UbuntuCorpusTrainer

model = ChatBot(name='robby',  
        logic_adapters=['chatterbot.logic.BestMatch'],
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        database_uri='sqlite:///database.sqliteRobby')

ubuntu_trainer = UbuntuCorpusTrainer(model)
ubuntu_trainer.train()


#### 

from chatbot import Robby
robby = Robby("Rob")

robby.mind.loadMindPalace('mindPalace.json')
robby.initiateTopic()

robby.markov.loadCorpus('convAI.json')
robby.mutter()

from markovChain import MarkovChain
m = MarkovChain()
m.loadCorpus('convAI.json')

robby.loadNeuralNetwork('intents.json')
robby.neuralNetResponse('hello')