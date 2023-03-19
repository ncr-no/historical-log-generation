import subprocess

class Powershell():
    """ Main class for executing powershell commands """
    def __init__(self):
       print('Class:Powershell Initialized')

    def download_file(self, url):
        """
          What:     Execute a powershell command.
          Purpose:  Download a specific file from an URL
        """
        try:
          subprocess.run(f'C:\Windows\System32\powershell.exe Invoke-Webrequest "{url}"', shell=True)
        except subprocess.CalledProcessError as e:
          print(e.output)
          raise ValueError("Error when downloading file")
        else:
           return True


    def upload_file(self, url, filepath):
        """
          What:     Execute a powershell command.
          Purpose:  Upload a file to an URL
        """
        try:
          subprocess.run(f"C:\Windows\System32\powershell.exe Invoke-WebRequest -uri {url} -Method Post -Infile {filepath} -ContentType 'application/zip'", shell=True)
        except subprocess.CalledProcessError as e:
          print(e.output)
          raise ValueError("Error when uploading file")
        else:
           return True
        