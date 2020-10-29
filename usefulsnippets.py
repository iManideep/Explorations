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



# "Pickling” is the process whereby a Python object hierarchy is converted into a byte stream, and 
# “unpickling” is the inverse operation, whereby a byte stream (from a binary file or bytes-like object) 
# is converted back into an object hierarchy.
import pickle
class testClass:
    def __init__(self,var1,var2):
        self.var1=var1
        self.var2=var2
#initiating a class object
testClassObject = testClass("Testing","pickle")
#loading class object into dictionary
test_dict={"testClassObject":testClassObject}
#using pickle to dump the dictionary object into pkl file(pickling)
with open("test.pkl","wb") as f:
    pickle.dump(test_dict,f)
#reading pkl file to retrieve dictionary object(unpickling)
with open("test.pkl","rb") as f:
    loaded_data=pickle.load(f)
#checking whethere information is retrieved back from pkl file
print(loaded_data)
print(loaded_data['testClassObject'].var1)
print(loaded_data['testClassObject'].var2)


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


#Generate QR Code
!pip install pyqrcode
!pip install pypng
import pyqrcode
s=input("Enter Text to generate QR Code:")
qr = pyqrcode.create(s)
qr.png(s+'.png',scale = 8)


# zip()
name = ["Nikhil","Shambhavi","Astha"] 
roll_no = [1,3,2] 
marks = [50, 60, 70] 
# zipping iterators name,roll_no,marks
mapped = zip(name, roll_no, marks) 
# mapped is a zip object converting it to a list 
mapped = list(mapped)
print("Zipped List Result : ",mapped) 
# zipping iterators
mapped_dict = zip(name, roll_no) 
# mapped is a zip object converting it to a dict
mapped_dict = dict(mapped_dict)
print("Zipped Dict Result : ",mapped_dict) 
# unzipping values 
namz, roll_noz, marksz = zip(*mapped) 
print("Unzipped Result : ") 
print("Name list is : ",end="") 
print(namz)
print("Roll Number list is : ",end="") 
print(roll_noz)
print("Marks list is : ",end="") 
print(marksz)


# filter()
a = [1,2,3,4,5,6]
# capturing only even numbers in a list 
# based on boolean returned by lambda 
# function inside filter
print(list(filter(lambda x: x%2==0,a)))


# reduce()
# apply a particular function passed in
# its argument to all of the list elements
# mentioned in the sequence passed along
from functools import reduce
print(reduce(lambda x,y:x*y,[1,2,3,4,5]))


# product()
# get cartesian product two iterables
from itertools import product
print(list(product([1,2,3],[4,5,6])))


# permutations()
# generate all possible permutations of an iterable
from itertools import permutations  
print(list(permutations(iterable=[1,2,3,4],r=2)))


# combinations()
# generate all possible combinations of an iterable
from itertools import combinations
print(list(combinations(iterable=[1,2,3,4],r=2)))


# groupby()
# returns key and iterable of grouped items
from itertools import groupby
L = [("a", 1), ("a", 2), ("b", 3), ("b", 4)] 
for key, group in groupby(iterable=L, key=lambda x: x[0]): 
    print(key + " :", list(group))
print("")
L = "AABBAAACCB"
for key, group in groupby(iterable=L): 
    print(key + " :", len(list(group)))


# Counter()
# keep the count of the elements in an iterable in the
# form of an unordered dictionary where the key represents
# the element in the iterable and value represents the 
# count of that element in the iterable
from collections import Counter 
counter_obj=Counter(['B','B','A','B','C','A','B','B','A','C'])
print(x)
for i,j in counter_obj.items():
    print(i,j)


# OrderedDict()
# It remembers the order in which the keys were inserted.
from collections import OrderedDict 
od = OrderedDict()
od['a'] = 1
od['b'] = 2
od['c'] = 3
od['d'] = 4
for key, value in od.items(): 
    print(key, value)


# Deque (Doubly Ended Queue) is the optimized list for quicker
# append and pop operations from both sides of the containe
from collections import deque 
de = deque([1,2,3]) 
print("Initial : ",de)
# using append() to insert element at right end 
de.append(4)
print("append(4) : ",de)
# using appendleft() to insert element at left end
de.appendleft(6) 
print("appendleft(6) : ",de)
# using pop() to delete element from right end 
de.pop() 
print("pop() : ",de) 
# using popleft() to delete element from left end 
de.popleft()
print("popleft() : ",de)


import sys
sys.exc_info()
# This function returns a tuple of (type, value, traceback) that give information
# about the exception that is currently being handled.
# If no exception is being handled anywhere on the stack, a tuple containing three None values is returned.
# type gets the exception type of the exception being handled (a class object)
# value gets the exception parameter 
# traceback gets a traceback object which encapsulates the call stack at the point where the exception originally occurred.

import traceback
traceback.format_exc()
# returns a string with exception information and stack trace entries from traceback object

try:
    [1,2,3][7]
except Exception as e:
    error = {
            "status":"error",
            "response":{
                "ErrorType":sys.exc_info()[0].__name__,
                "Message":str(sys.exc_info()[1]),
                "Traceback":traceback.format_exc()
            }
    }