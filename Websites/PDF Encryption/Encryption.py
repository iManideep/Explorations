# https://pythonbasics.org/flask-upload-file/
# https://stackoverflow.com/questions/24612366/delete-an-uploaded-file-after-downloading-it-from-flask

from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import os
import io
from PyPDF2 import PdfFileWriter, PdfFileReader
app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('index.html', message = "")
    elif request.method == 'POST':
        try:
            for file in os.listdir():
                if file.endswith(".pdf"):
                    os.remove(file)
            if 'password' not in request.form:
                return render_template('index.html', message = "Please enter password before submitting")
            password = request.form.get('password')
            if password.replace(" ","") == "":
                return render_template('index.html', message = "Please enter password before submitting")
            if 'EncryptionType' not in request.form:
                return render_template('index.html', message = "Please select type of encryption before submitting")
            EncryptionType = request.form.get('EncryptionType')
            f = request.files['file']
            if f.filename.replace(" ","") == "":
                return render_template('index.html', message = "Please upload a PDF file before submitting")
            f.save(secure_filename(f.filename))
            fileName = f.filename.replace(" ","_").replace("(","").replace(")","")
            if not fileName.endswith(".pdf"):
                os.remove(fileName)
                return render_template('index.html', message = "Please upload PDF files only")
            if EncryptionType == "decrypt":
                if os.path.isfile(fileName):
                    opened_file = open(fileName,'rb')
                    encrypt_pdf = PdfFileReader(opened_file)
                    if encrypt_pdf.isEncrypted:
                        if encrypt_pdf.decrypt(password):
                            decrypt_pdf = PdfFileWriter()
                            for i in range(encrypt_pdf.getNumPages()):
                                decrypt_pdf.addPage(encrypt_pdf.getPage(i))
                            with open(f"decrypted_{fileName}","wb") as f:
                                decrypt_pdf.write(f)
                            opened_file.close()
                            os.remove(fileName)

                            return_data = io.BytesIO()
                            with open(f"decrypted_{fileName}", 'rb') as fo:
                                return_data.write(fo.read())
                            return_data.seek(0)

                            os.remove(f"decrypted_{fileName}")

                            return send_file(return_data, mimetype = 'application/pdf',
                                            attachment_filename = f"decrypted_{fileName}", as_attachment = True)
                            
                        else:
                            opened_file.close()
                            os.remove(fileName)
                            return render_template('index.html', message = "Please enter correct password")
                    else:
                        opened_file.close()
                        os.remove(fileName)
                        return render_template('index.html', message = "Please upload a PDF with encryption")
                else:
                    return render_template('index.html', message = "File doesn't exists")
            
            elif EncryptionType == "encrypt":
                if os.path.isfile(fileName):
                    opened_file = open(fileName,'rb')
                    input_file = PdfFileReader(opened_file)
                    if not input_file.isEncrypted:
                        encrypted_file = PdfFileWriter()
                        for page in range(input_file.numPages):
                            encrypted_file.addPage(input_file.getPage(page))
                        encrypted_file.encrypt(password)
                        with open(f"encrypted_{fileName}",'wb') as f:
                            encrypted_file.write(f)
                        opened_file.close()
                        os.remove(fileName)

                        return_data = io.BytesIO()
                        with open(f"encrypted_{fileName}", 'rb') as fo:
                            return_data.write(fo.read())
                        return_data.seek(0)

                        os.remove(f"encrypted_{fileName}")

                        return send_file(return_data, mimetype = 'application/pdf',
                                        attachment_filename = f"encrypted_{fileName}", as_attachment = True)
                    else:
                        opened_file.close()
                        os.remove(fileName)
                        return render_template('index.html', message = "Please upload a PDF without encryption")
                else:
                    return render_template('index.html', message = "File doesn't exists")
        except:
            return render_template('index.html', message = "Some error occured. Please try again")
		
if __name__ == '__main__':
    app.run(debug = True)