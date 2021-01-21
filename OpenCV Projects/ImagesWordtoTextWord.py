import tempfile
import zipfile
import os
import pytesseract
import html
import cv2
import shutil
from docx import Document
import os

absolute_path = os.path.abspath(__file__+"/..")
#path for word document to be worked on
word_path=  absolute_path + "/test_images/word.docx"
#tesseract executable path
pytesseract.pytesseract.tesseract_cmd = absolute_path + "/../../../AppData/Local/Tesseract-OCR/tesseract.exe"

#extracts text from image 
def image_to_text_converter(path):
    #reading image
    img = cv2.imread(path)
    #converting image to grayscale
    imgWarpGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #using pytesseract package to extract text from image
    para_string = pytesseract.image_to_string(imgWarpGray)
    para_string = para_string.replace("\n"," ")
    #add paragraph to word document
    document.add_paragraph(para_string)

#returns list of all files in a directory and sub-directories
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

#unzips a word document into a temp directory
def document_extractor(file):
    extract_dir = tempfile.mkdtemp()
    zip_ref = zipfile.ZipFile(file, "r")
    zip_ref.extractall(extract_dir)
    zip_ref.close()
    return extract_dir

#unzip word document provided
temp_folder_path=document_extractor(word_path)
#navigating to folder containing images inside extracted directory
media_path=temp_folder_path+"\\word\\media"
#accessing images inside the word document
list_of_image_paths=getListOfFiles(media_path)

#creating an blank word document
document = Document()

#extracting text from each image and adding it as paragraph into word document
for image_path in list_of_image_paths:
    image_to_text_converter(image_path)

#saving word document
document.save('demo.docx')
#deleting temporary folder
shutil.rmtree(temp_folder_path)