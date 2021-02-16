# https://pythonbasics.org/flask-upload-file/
# https://stackoverflow.com/questions/24612366/delete-an-uploaded-file-after-downloading-it-from-flask

from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import os
import io
from PyPDF2 import PdfFileWriter, PdfFileReader
app = Flask(__name__)

@app.route('/decrypt', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('index.html',message="")
    elif request.method == 'POST':
        password = request.form.get('password')
        f = request.files['file']
        f.save(secure_filename(f.filename))
        fileName = f.filename
        if not fileName.endswith(".pdf"):
            os.remove(fileName)
            return render_template('index.html',message="Please upload PDF files only")
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
                    return render_template('index.html',message = "Wrong Password")
            else:
                opened_file.close()
                os.remove(fileName)
                return render_template('index.html',message = "PDF is not Encrpyted")
        else:
            return render_template('index.html',message = "File doesn't exists")
		
if __name__ == '__main__':
    app.run(debug = True)