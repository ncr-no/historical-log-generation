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
    currenttime = 0
    def __init__(self,interval,shift):
        print('Class:Clock Initialized')
        self.time_machine = SetInterval(interval, 
                                        self.moveTime, 
                                        args=([shift]))
        self.time_machine.daemon = True
          
    def set_clock(self, epoch):
        time = datetime.datetime.fromtimestamp(epoch)
        print(time)
        win32api.SetSystemTime(time.year,time.month,0,
                               time.day,time.hour,time.minute,time.second,time.microsecond)
        return True

    def moveTime(self, time):
        tt = datetime.datetime.utcnow()
        tt = tt + datetime.timedelta(seconds=int(time)) # add the delta
        currenttime = tt.timestamp()
        win32api.SetSystemTime(tt.year, tt.month, 0, tt.day,
                               tt.hour, tt.minute,tt.second, 0)

    def start_time_machine(self):
        self.time_machine.start()
        print("Time machine started")

    def stop_time_machine(self):
        self.time_machine.cancel()
        print("Time machine stopped")

if __name__ == '__main__':
    clock = Clock(1,2)
    clock.start_time_machine()
    sleep(60)
    clock.stop_time_machine()