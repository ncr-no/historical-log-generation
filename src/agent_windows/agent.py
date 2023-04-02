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

fields = {'name':clean_name,'email':clean_email}

for key in fields:
    fields[key]()





class Agent():
    """ Main class for administering the agent """
    currenttime = 0
    timeline = timeline
    timehit = False
    
    def __init__(self):
        self.browser = Browser()
        self.powershell = Powershell()
        self.clock = Clock(0.1,1)

        methods = { 
            'browse_url': self.browser.browse_url, 
            'search_google':self.browser.search_google, 
            'upload_file':self.powershell.upload_file,
            'download_file':self.powershell.download_file
            }
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

        # For each day in the timeline
        for idx,day in timeline:
            print(day["date"])

            # For each event in a day 
            for event in timeline[idx]["events"]:
                print('New event:')
                print(json.dumps(event, indent=2))

                # Will stay at timeCheck until its time to do next event
                self.timeCheck(event["clock"][1])
                
                #Time for event is hit. Stop and do action:
                self.clock.stop_time_machine()
                #methods[event["method"]](event["options"][0]) # TO BE TESTED
                self.browser.search_google(event["options"][0])
                self.timeHit = False
                self.clock.start_time_machine()    
  
    def getTimeline(self):
        print('getTimeline()')
        #call generate timeline function

if __name__ == '__main__':
    agent = Agent()
    
    threading.Thread(target=agent.generate(), daemon=True).start()
    #agent.browser.search_google("how to slay a dragon")
    #agent.clock.test()
    #agent.browser.search_google("kakeoppskrift")