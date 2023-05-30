import json
import socket
from flask import Flask
from flask import request
import argparse
import datetime
import scheduler 
from threading import Thread
import ctypes, os
from time import sleep
from modules.clock import Clock
from modules.browser import Browser
from modules.powershell import Powershell
from services.system_service import System

app = Flask(__name__)
api_service = None

parser=argparse.ArgumentParser()
os.environ['WDM_SSL_VERIFY']='0'

#specify encoding to avoid UnicodeDecodeError


@app.route('/create', methods=['POST'])
def api():
    agent.setargs(request.args.get('start'),request.args.get('stop'),request.args.get('schedule'),request.args.get('speed'))
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
        self.clock = Clock()
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
          self.system.set_capture_mode()
          scheduler.gen_timeline(self.start, self.stop,self.schedule)
          self.getTimeline()
        except Exception as e:
          print('BREAKING ERROR')
          raise SystemExit(e)
  
    
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
        stopday = datetime.datetime.strptime(self.stop + ' 23:59:59', "%d/%m/%Y %H:%M:%S").timestamp()
        
        try:
          self.clock.set_clock(startday)
        except Exception as e:
          raise SystemExit(e)
        self.clock.start_time_machine()
        self.system.start_windump()
        self.timeHit = False

        for idx, day in enumerate(self.timeline):
          print('Looking for events at day:',idx)
          for event in self.timeline[idx]["events"]:
              print('New event:')
              print(json.dumps(event, indent=2))
              self.timeCheck(event["clock"][1])
              self.clock.stop_time_machine()

              self.dynamic_call(event["module"], event["method"], event["options"])

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

    def dynamic_call(self, module, method, options):
      # Call a function dynamically based on the module and method name
      # Create a dictionary that maps module names to instances
      modules = {
          'browser': Browser(),
          'powershell': Powershell()
      }

      # Get the module instance and method
      module_instance = modules.get(module, None)
      
      # Check if the module exists
      if not module_instance:
          print(f"No such module: {module}")
          return

      # Get the method from the class based on the supplied method name
      method_to_call = getattr(module_instance, method, None)

      #Check if the method exists
      if not method_to_call:
          print(f"No such method: {method} in module: {module}")
          return

      # Call the method with arguments
      method_to_call(options)


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
    parser.add_argument('--speed', help='Speed multiplier (1-30)',metavar='{10-30}')
    
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
            exit()
        else:
            if args.speed != "10" and args.speed != "20" and args.speed != "30":
                print('Speed multiplier is not 10/20/30')
                exit()
            agent.setargs(args.start,args.stop,args.schedule,args.speed)
            agent.clock.set_args(0.1,args.speed)
            agent.prepare()
            agent.thread = Thread(target=agent.generate(), daemon=True).start()

    agent.system.stop_windump()
    agent.system.enable_ntp()
    print('END')