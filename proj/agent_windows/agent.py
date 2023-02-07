import json
import datetime
from types import SimpleNamespace
from module.browser import Browser
from module.clock import Clock

#specify encoding to avoid UnicodeDecodeError
with open('./timeline.json') as f:
    timeline = json.load(f)
    #print(json.dumps(timeline, indent=2))
#time = datetime.datetime.fromtimestamp(event.)
#for event in timeline:
#    print(event)

class Agent():
    """ Main class for browsing websites using chrome """
    def __init__(self):
        self.browser = Browser()
        self.clock = Clock()

    def register(self):
        pass
if __name__ == '__main__':
    agent = Agent()
    agent.clock.test()
    #agent.browser.search_google("kakeoppskrift")