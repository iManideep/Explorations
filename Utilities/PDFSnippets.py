# decrypt PDF file
import os
from PyPDF2 import PdfFileWriter, PdfFileReader
fileName = input()
if os.path.isfile(fileName):
    encrypt_pdf = PdfFileReader(open(fileName,'rb'))
    if encrypt_pdf.isEncrypted:
        password = input()
        if encrypt_pdf.decrypt(password):
            decrypt_pdf = PdfFileWriter()
            for i in range(encrypt_pdf.getNumPages()):
                decrypt_pdf.addPage(encrypt_pdf.getPage(i))
            with open(f"decrypted_{fileName}","wb") as f:
                decrypt_pdf.write(f)
        else:
            print("Wrong Password")
    else:
        print("PDF is not encrpyted")
else:
    print("File doesn't exists")



# reverse pages order in PDF
import os
from PyPDF2 import PdfFileWriter, PdfFileReader
fileName = input()
if os.path.isfile(fileName):
    output_pdf = PdfFileWriter()
    with open(fileName, 'rb') as readfile:
        input_pdf = PdfFileReader(readfile)
        total_pages = input_pdf.getNumPages()
        for page in range(total_pages - 1, -1, -1):
            output_pdf.addPage(input_pdf.getPage(page))
        with open(f'reversed_{fileName}', "wb") as writefile:
            output_pdf.write(writefile)
else:
    print("File doesn't exists")


# merge PDFs
from PyPDF2 import PdfFileWriter, PdfFileReader
# add names of required PDFs into 'files' list
files = []
output_pdf = PdfFileWriter()
for file in files:
    input_pdf = PdfFileReader(file)
    total_pages = input_pdf.getNumPages()
    for page in range(total_pages):
        output_pdf.addPage(input_pdf.getPage(page))
with open('merged.pdf', "wb") as writefile:
    output_pdf.write(writefile)