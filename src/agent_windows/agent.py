import json
from time import sleep
import socket
import threading
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
    timehit = False
    
    def __init__(self):
        self.browser = Browser()
        self.clock = Clock(0.1,1)
        sleep(2)
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

    def timeCheck(self,eventTime):
        while not self.timeHit:
            print(self.timehit)
            print(eventTime, self.clock.currenttime)
            if(eventTime < self.clock.currenttime):
                self.timeHit = True
                return True
            else:
                sleep(1)
        return


    def generate(self):
        startday = 1641196325
        stopday = 1641254400
        self.clock.set_clock(startday)
        self.clock.start_time_machine()
        
        print(self.clock.currenttime)
        print(len(timeline[0]['events']))
        self.timeHit = False
        for event in timeline[0]["events"]:
            print('New event:')
            print(json.dumps(event, indent=2))
            self.timeCheck(event["clock"][1])
            #Time for event is hit:

            self.clock.stop_time_machine()
            self.browser.search_google(event["options"][0])
            self.timeHit = False
            self.clock.start_time_machine()
                
        #while(nextevent.clock < self.currenttime):
            #read system time every 1 second
        #    self.currenttime = self.clock.get_time()

        
  
    def getTimeline(self):
        print('getTimeline()')
        #call generate timeline function

if __name__ == '__main__':
    agent = Agent()
    
    threading.Thread(target=agent.generate(), daemon=True).start()
    #agent.browser.search_google("how to slay a dragon")
    #agent.clock.test()
    #agent.browser.search_google("kakeoppskrift")