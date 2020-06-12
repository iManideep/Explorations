import json
#string to dictionary or list
json.loads('string')
#dictionary or list to string
json.dumps(dict)
#dictionary or json structure to visualize
x=json.dumps(dict,indent=4)
with open('new.json','w') as f:
    f.write(x)


#xml structure to visualize
!pip install lxml
from lxml import etree
def xml_printer(string):
    root=etree.XML(string.encode('utf-8'))
    xml_str="".join([etree.tostring(root, encoding="unicode", pretty_print=True)])
    with open('test.xml','w') as f:
        f.write(xml_str)


#youtube search api
!pip install google-api-python-client
from apiclient.discovery import build
youtube=build('youtube','v3',developerKey=api_key)
res=youtube.search().list(q="avengers",part="snippet",type="video").execute()
res['items']


#api response
!pip install requests
import requests
params={'a':'b'}
data={'x':'y'}
url="http:/127.0.0.1/"
#for get request
response=requests.get(url,params)
#for post request
response=requests.post(url,data)
#get json out of response
response.json()


#for webscrapping
!pip install beautifulsoup4
from bs4 import BeautifulSoup
soup=BeautifulSoup('html/xml','html5lib')
#first occurance of 'a' tag
soup.find('a')
#list of all occurances of 'a' tag
soup.findAll('p')


import pandas as pd
#dataframe to html table
df.to_html(columns=df.columns)
#dataframe to json
df.to_json(orient='index')
#find which columns has NA
df.isnull().sum()


#accessing windows clipboard content
import win32clipboard
win32clipboard.OpenClipboard()
print(win32clipboard.GetClipboardData())
win32clipboard.CloseClipboard()


#Decorators - Function takes another function as argumentand adds some kind
#of functionality and returns function without altering source code of function
# Source Link - https://www.youtube.com/watch?v=FsAPt_9Bf3U

#simple example for decorator function
def decorator_function(function):
    def wrapper_function(*args,**kwargs):
        print("Running {} using decorator".format(function.__name__))
        return function(*args,**kwargs)
    return wrapper_function
#decorator function for logging
def my_logger(orig_func):
    import logging
    logging.basicConfig(filename='{}.log'.format(orig_func.__name__), level=logging.INFO)
    def wrapper(*args, **kwargs):
        logging.info('Ran with args: {}, and kwargs: {}'.format(args, kwargs))
        return orig_func(*args, **kwargs)
    return wrapper
#decorator function for calculationg execution time
def my_timer(orig_func):
    import time
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = orig_func(*args, **kwargs)
        t2 = time.time() - t1
        print('{} ran in: {} sec'.format(orig_func.__name__, t2))
        return result
    return wrapper
#decorator function for exception handling
def handle_exception(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print(e)
    return wrapper
#using decorator function on a function
@decorator_function
def test_function(name,city):
    return f"({name},{city})"


import os
#get all files in a directory
os.listdir('directory_name')
#list of file paths for all files in the directory
def getListOfFiles(dirName):
    listOfFile = os.listdir(dirName)
    allFiles = list()
    for entry in listOfFile:
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)                
    return allFiles

