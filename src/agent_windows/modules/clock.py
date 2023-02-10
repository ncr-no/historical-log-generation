from win32 import win32api
class Clock():
    def __init__(self):
        print('asd')
        
    def set_clock(self, year,month,dayofweek,day,hour,minute,second,millisecond):
        win32api.SetSystemTime(year,month,dayofweek,day,hour,minute,second,millisecond)
   
    def test(self):
        print('suceess')