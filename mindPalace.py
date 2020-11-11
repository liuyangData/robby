
import string


class MindPalace:
    
    mindPalace = {'me':{},
                'you':{},
                'universe':{}}  

    def __init__(self):
        pass

    def addEntry(self, area, entry):
        area[entry[0]] = entry[1]
    
    def loadMindPalace(self, file):
        import json
        with open(file, 'r') as f:
            self.mindPalace = json.load(f)

    def find(self, ls, text):
        obj = ''
        for item in ls:
            if item in text:
                obj = item
        return obj

    def remove(self, text, words):
        for word in words:
            text = text.replace(word, '')
        return text

    def askHobby(self):
        print("Are you a sporty person?")
        res = input().lower()
        if  'y' in res:
            print("Cool, what kind of sport?")
            res = input().lower()
            sport = self.find(self.mindPalace['universe']['hobbies'].keys(), res)
            if sport != '':
                print("Me too, it's nice to " + self.mindPalace['universe']['hobbies'][sport] )
            elif 'swimming' in res:
                print("Where do you swim? In the pool or in the ocean?")
                res = input().lower()
                if "pool" in res:
                    print("Nice. I can do 20 laps in a standard pool")
                elif "ocean" in res:
                    print("That's nuts, beware of sea monsters!")
                else:
                    print("Where is that? I havnt heard of it before, could you elaborate?")
                    res = input().lower()
            else:
                print("Sorry, could you repeat the name of your hobby?")
                obj = input().lower()
                print("Interesting, so what is " + obj + "?")
                res = input().lower()
                res = self.remove(res, ['oh ', 'it is ', "it's "])
                print("I see, today I have learnt that " + obj + " is " + res)
                self.addEntry(self.mindPalace['you']['hobbies'], (obj, res))
                self.addEntry(self.mindPalace['universe']['hobbies'], (obj, res))
        else:
            print("I see, what is your hobby then?")

# mind = MindPalace()
# mind.loadMindPalace('mindPalace.json')
# mind.askHobby()
# mind.mindPalace