import subprocess
import os  
import time

class System():
    capture = None

    def __init__(self):
        print('Class:System_service Initialized')


    def start_windump(self):
      """
        What:     Start subprocess
        Purpose:  Start the capture of packets with windump
        Will rotate capture-file every 1GB. 1000 * 1M bytes = 1G with -C flag
      """
      
      try:
        full_path = os.path.realpath(__file__) # Get full path of this file
        os.path.dirname(full_path)            # Get directory name
        
        #Windump path using fullpath of this file:
        wdump_path = os.path.dirname(full_path) + '\\windump.exe'
        print(wdump_path)

        self.capture = subprocess.Popen([wdump_path, '-i','1','-w','../../../output/captured.pcap','-C','1000'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            creationflags=subprocess.CREATE_NEW_CONSOLE)
        self.capture.wait()
        time.sleep(10)
      except:
        raise ValueError("Error occured when starting windump")
      else:
        print('Windump started')
        return True
  

    def stop_windump(self):
      """
        What:     Killing capture subprocess
        Purpose:  Stop the capture of packets with windump
      """
      try:
        self.capture.kill()
      except:
        raise ValueError("Error occured when stopping windump")
      else:
        print('Windump stopped')
        return True
      

    def disable_ntp(self):
        """
          What:     Disable the NTP sync service on Windows.
          Purpose:  Make sure client does not sync during run.
        """
        try:
          subprocess.run(r'powershell.exe Set-ItemProperty HKLM:\SYSTEM\CurrentControlSet\services\W32Time\Parameters -Name "Type" -Value "NoSync"', shell=True, check=True, stderr=subprocess.PIPE)
        except Exception as e:
          raise ValueError(e)
        else:
           print('NTP disabled')
           return True
        
    
    def enable_ntp(self):
        """
          What:     Enable the NTP sync service on Windows.
          Purpose:  After creating logs. Enable NTP again.
        """
        try:
          subprocess.run(r'powershell.exe Set-ItemProperty HKLM:\SYSTEM\CurrentControlSet\services\W32Time\Parameters -Name "Type" -Value "NTP"', shell=True, check=True, stderr=subprocess.PIPE)
        except Exception as e:
          raise ValueError(e)
        else:
           print('NTP enabled')
           return True


if __name__ == '__main__':
    system = System()
    try:
      system.disable_ntp()
    except Exception as e:
      raise SystemExit(e)
    else:
       True