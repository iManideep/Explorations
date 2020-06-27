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

#logging
# DEBUG: Detailed information, typically of interest only when diagnosing problems.
# INFO: Confirmation that things are working as expected.
# WARNING: An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.
# ERROR: Due to a more serious problem, the software has not been able to perform some function.
# CRITICAL: A serious error, indicating that the program itself may be unable to continue running.
# https://www.youtube.com/watch?v=-ARI4Cz-awo
#for logger format refer - https://docs.python.org/3/library/logging.html#logrecord-attributes
import logging
import sys
from logging.handlers import TimedRotatingFileHandler
FORMATTER = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger_obj=logging.getLogger("Logger-Name")
logger_obj.setLevel(logging.DEBUG)
#for printing in console
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(FORMATTER)
logger_obj.addHandler(console_handler)
#for creating a log file
file_handler = TimedRotatingFileHandler("myloggerfile.log",when="midnight",encoding="utf-8")
file_handler.setFormatter(FORMATTER)
logger_obj.addHandler(file_handler)


import os
import img2pdf
#A4 Size paper dimensions 210mm x 297mm
#img2pdf.mm_to_pt() converts millimeter to point
a4inpt = (img2pdf.mm_to_pt(210),img2pdf.mm_to_pt(297))
layout_fun = img2pdf.get_layout_fun(pagesize=a4inpt)
#Input directory name
DIR_PATH="../Documents"
file_name=DIR_PATH.split("/")[-1]+".pdf"
with open(file_name,"wb") as f:
    f.write(img2pdf.convert([i for i in os.listdir(DIR_PATH) if i.endswith(".jpg")], layout_fun=layout_fun))


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

