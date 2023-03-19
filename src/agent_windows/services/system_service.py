import subprocess

class System():
    def __init__(self):
        print('System service initialized')
    
    def disable_ntp(self):
        """
          What:     Disable the NTP sync service on Windows.
          Purpose:  Make sure client does not sync during run.
        """
        try:
          subprocess.run(r'C:\Windows\System32\Windll\v1.0\powershell.exe Set-ItemProperty HKLM:\SYSTEM\CurrentControlSet\services\W32Time\Parameters -Name "Type" -Value "NoSync"', shell=True)
        except subprocess.CalledProcessError as e:
          print(e.output)
          raise ValueError("Error occured when disabling NTP")
        else:
           return True
        
    
    def enable_ntp(self):
        """
          What:     Enable the NTP sync service on Windows.
          Purpose:  After creating logs. Enable NTP again.
        """
        try:
          subprocess.run(r'C:\Windows\System32\Windll\v1.0\powershell.exe Set-ItemProperty HKLM:\SYSTEM\CurrentControlSet\services\W32Time\Parameters -Name "Type" -Value "NTP"', shell=True)
        except subprocess.CalledProcessError as e:
          print(e.output)
          raise ValueError("Error occured when disabling NTP")
        else:
           return True
    
if __name__ == '__main__':
    system = System()
    print(system.disable_ntp())
