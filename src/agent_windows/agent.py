import json
import datetime
from time import sleep
import platform
import socket
from types import SimpleNamespace
from modules.browser import Browser
from modules.clock import Clock
from services.system_service import System
#import services.api_service

#specify encoding to avoid UnicodeDecodeError
with open('timeline.json') as f:
    timeline = json.load(f)
    #print(json.dumps(timeline, indent=2))
    #time = datetime.datetime.fromtimestamp(event.)
    
    #print(json.dumps(timeline[0]["events"], indent=2, sort_keys=True, default=str))

class Agent():
    """ Main class for administering the agent """
    currenttime = 0
    timeline = timeline
    
    def __init__(self):
        self.browser = Browser()
        self.clock = Clock(1,2)
        self.generate()
        #self.timeline = timeline


    def register(self):
        print('RUN')
        """ 
            Register at master. Send system name etc
            Receive timeline of events
        """
        return
    
    def get_system_info(self):
        #hostname = platform.uname()[1]
        hostname = socket.gethostname()
        fqdn = socket.getfqdn()
        return hostname,fqdn

    def generate(self):
        startday = 1641168000
        stopday = 1641254400
        self.clock.set_clock(startday)
        self.clock.start_time_machine()
        
        for event in timeline[0]["events"]:
            
            while event["clock"][1] < self.clock.currenttime:
                self.clock.stop_time_machine()
                print('true')
                
        #while(nextevent.clock < self.currenttime):
            #read system time every 1 second
        #    self.currenttime = self.clock.get_time()

        
  
    def getTimeline(self):
        print('getTimeline()')
        #call generate timeline function

if __name__ == '__main__':
    agent = Agent()
    print(agent.get_system_info())
    print('testtetstetset')
    #agent.browser.search_google("how to slay a dragon")
    #agent.clock.test()
    #agent.browser.search_google("kakeoppskrift")