import subprocess

class Powershell():
    """ Main class for browsing websites using chrome """
    #def __init__(self):

    def download_file(self, url):
        """ Function for download a specific file from an URL """
        subprocess.call(f'C:\Windows\System32\powershell.exe Invoke-Webrequest "{url}"', shell=True)
    
    def upload_file(self, url, file):
        """ Function for upload a specific file from an URL """
        subprocess.call(f'')
        