from win32 import win32api
from threading import Timer
from time import sleep
import datetime

# Creating similar functionality as setInterval in javascript
# https://stackoverflow.com/questions/12435211/threading-\
# timer-repeat-function-every-n-seconds
class SetInterval(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


class Clock():
    time_machine = None
    currenttime = 2
    def __init__(self):

        print('Class:Clock Initialized')
        self.currenttime = datetime.datetime.utcnow().timestamp()
    def set_args(self, interval, shift):
        self.interval = interval
        self.shift = shift
        
    def set_clock(self, epoch):
        time = datetime.datetime.fromtimestamp(epoch)
        try:
            win32api.SetSystemTime(time.year,time.month,0,
                                   time.day,time.hour,time.minute,time.second,time.microsecond)
        except Exception as e:
            raise ValueError(e)
        else:
            self.currenttime = datetime.datetime.utcnow().timestamp()
            return True
        
    def moveTime(self, time):
        tt = datetime.datetime.utcnow()
        tt = tt + datetime.timedelta(seconds=int(time)) # add the delta
        self.currenttime = tt.timestamp()
        
        try:
            win32api.SetSystemTime(tt.year, tt.month, 0, tt.day,
                                  tt.hour, tt.minute,tt.second, 0)
        except Exception as e:
            raise ValueError(e)
        else:
          return True

    def start_time_machine(self):
        self.time_machine = SetInterval(self.interval, 
                            self.moveTime, 
                            args=([self.shift]))
        
        self.time_machine.daemon = True
        self.time_machine.start()
        print("> Time machine started")

    def stop_time_machine(self):
        self.time_machine.cancel()
        print("> Time machine stopped")

if __name__ == '__main__':
    clock = Clock(1,2)
    clock.start_time_machine()
    sleep(60)
    clock.stop_time_machine()