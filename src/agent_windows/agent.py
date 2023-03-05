import json
import datetime
import platform
import socket
from types import SimpleNamespace
#from modules.browser import Browser
#from modules.clock import Clock

#specify encoding to avoid UnicodeDecodeError
with open('./timeline.json') as f:
    timeline = json.load(f)
    #print(json.dumps(timeline, indent=2))
#time = datetime.datetime.fromtimestamp(event.)
#for event in timeline:
#    print(event)

class Agent():
    """ Main class for administering the agent """
    currenttime = 0
    timeline
    
    def __init__(self):
        #self.browser = Browser()
        #self.clock = Clock()
        self.timeline = timeline

    def register(self):
        """ 
            Register at master. Send system name etc
            Receive timeline of events
        """
        pass
    
    def get_system_info(self):
        #hostname = platform.uname()[1]
        hostname = socket.gethostname()
        fqdn = socket.getfqdn()
        return hostname,fqdn

    def startGen(self):
        for event in self.timeline:
          print(event)
    
    def getTimeline(self):
        print('getTimeline()')
        #call generate timeline function

if __name__ == '__main__':
    agent = Agent()
    print(agent.get_system_info())

    #agent.clock.test()
    #agent.browser.search_google("kakeoppskrift")