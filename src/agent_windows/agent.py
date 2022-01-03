import json
import socket
from flask import Flask
from flask import request
import argparse
import sys
import datetime
import scheduler 
from threading import Thread
import ctypes, os
from time import sleep
from modules.clock import Clock
from modules.browser import Browser
from services.system_service import System

app = Flask(__name__)
api_service = None

parser=argparse.ArgumentParser()
os.environ['WDM_SSL_VERIFY']='0'

#specify encoding to avoid UnicodeDecodeError


@app.route('/create', methods=['POST'])
def api():
    agent.setargs('01012022','04012022','normal',30)
    agent.prepare()
    
    agent.thread = Thread(target=agent.generate(), daemon=True)
    agent.thread.start()
    return('true')



class Agent():
    """ Main class for administering the agent """
    currenttime = 0
    timehit = False
    thread = None
    
    def __init__(self):
        # Command line arguments
        print('##################')
        self.browser = Browser()
        self.clock = Clock(0.1,2)
        self.system = System()
        print('##################')
        sleep(2)
        #self.timeline = timeline


    def setargs(self,start,stop,schedule,speed):
        self.start = start
        self.stop = stop
        self.schedule = schedule
        self.speed = speed
        
    def prepare(self):
        try:
          self.system.disable_ntp()
          self.system.start_windump()
          scheduler.gen_timeline(self.start, self.stop,'normal')
          self.getTimeline()
        except Exception as e:
          print('BREAKING ERROR')
          raise SystemExit(e)


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
            print('Client clock seconds until next event:',eventTime - int(self.clock.currenttime))
            if(eventTime < self.clock.currenttime):
                print('> EVENT TIME HIT')
                self.timeHit = True
                return True
            else:
                sleep(1)
        return


    def generate(self):
        startday = datetime.datetime.strptime(self.start, "%d/%m/%Y").timestamp()
        stopday = datetime.datetime.strptime(self.start + ' 23:59:59', "%d/%m/%Y %H:%M:%S").timestamp()
        print(stopday)
        try:
          self.clock.set_clock(startday)
        except Exception as e:
          raise SystemExit(e)
        self.clock.start_time_machine()
        
        self.timeHit = False
        for idx, day in enumerate(self.timeline):
          print('Looking for events at day:')
          print(idx)
          for event in self.timeline[idx]["events"]:
              print('New event:')
              print(json.dumps(event, indent=2))
              self.timeCheck(event["clock"][1])
              #Time for event is hit:

              self.clock.stop_time_machine()
              self.browser.search_google(event["options"][0])
              self.timeHit = False
              self.clock.start_time_machine()

        # No more events. Run until stop date, end of day
        self.timeCheck(stopday)
        self.clock.stop_time_machine()
        print('> END OF GENERATE')
        
  
    def getTimeline(self):
        print('getTimeline()')
        with open('timeline.json') as f:
          self.timeline = json.load(f)

def isAdmin():
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin

agent = Agent()

if __name__ == '__main__':   
    if isAdmin():
        print("SYSTEM: Is admin, continuing.")
    else:
        print("SYSTEM: Administrator privileges are required to run this program.")
        exit()
        
      # Argument for API
    parser.add_argument('--api', action='count', default=0)
    # Argument for start and stop date in format ddmmyyyy, work schedule and multiplier speed
    parser.add_argument('--start', metavar='DD/MMY/YYY',help='Start date')
    parser.add_argument('--stop',  metavar='DD/MM/YYYY',help='End date')
    parser.add_argument('--schedule', choices=['normal','247'],help='Which work-schedule to use') 
    parser.add_argument('--speed', help='Speed mult iplier (1-30)',metavar='{10-30}')
    
    #parse args
    args=parser.parse_args()
    if(args.api == 1):
        print('API')
        api_service = Thread(target=app.run,kwargs={'port':8080})
        api_service.start()
        print('> API stopped')

    else:
        if None in (args.start,args.stop,args.schedule,args.speed):
            print('Missing arguments. Check --help for more info')
        else:
            agent.setargs(args.start,args.stop,args.schedule,args.speed)
            agent.prepare()
            agent.thread = Thread(target=agent.generate(), daemon=True).start()
    agent.system.enable_ntp()
    print('END')