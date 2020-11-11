from chatbot import Chatbot
import json
import random

agents = ["IR", "ML", "RB", "HM"]

for agent in random.shuffle(agents) :

    ### Information Retrieval System

    if agent == 'IR':

        print("Say something")

        from chatbot import IR_Bot

        ir = IR_Bot('ir')
        ir.loadDictJson('irDictionary.json')

        userResponse = input()
        while 'quit' not in userResponse:
            print(ir.reply(userResponse))
            userResponse = input()


    # Machine Learning Bot

    if agent == 'ML':

        print("Say something:")

        from chatbot import ML_Bot

        ml = ML_Bot("ML")
        ml.trainJSON('convAI.json')

        userResponse = input()
        while 'quit' not in userResponse:
            print(ml.reply(userResponse))
            userResponse = input()


    # Hybrid Chatbot: Robby

    if agent == 'RB':


        from chatterbot import ChatBot
        from chatbot import Robby
        robby = Robby("Rob")

        robby.mind.loadMindPalace('mindPalace.json')
        robby.initiateTopic()

        robby.markov.loadCorpus('convAI.json')

        from markovChain import MarkovChain
        m = MarkovChain()
        m.loadCorpus('convAI.json')

        robby.loadNeuralNetwork('intents.json')

        print("Say something:")
        res = input()

        while res != 'bye':
            print(robby.neuralNetResponse(res))
            res = input()
            
        
    ### Human Chat
    if agent == 'HM': 
        print("Say something")
        userResponse = input()
        while 'quit' not in userResponse:
            print(getInput())
            userResponse = input()

           




