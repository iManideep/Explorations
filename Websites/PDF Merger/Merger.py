from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import io
from PyPDF2 import PdfFileWriter, PdfFileReader
app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('Merger.html', message = "")
    elif request.method == 'POST':
        try:
            for file in os.listdir():
                if file.endswith(".pdf"):
                    os.remove(file)
            uploaded_files = request.files.getlist("filelist")
            if uploaded_files[0].filename == "":
                return render_template('Merger.html', 
                            message = "Please upload PDF files before submitting")
            name_list = []
            actual_name_list = []
            for file in uploaded_files:
                actual_name_list.append(file.filename)
                name_list.append(file.filename.replace(" ","_").replace("(","").replace(")",""))
                file.save(secure_filename(file.filename))
            
            if not all(map(os.path.isfile, name_list)):
                return render_template('Merger.html', 
                            message = "Upload wasn't successful. Please try again")
            
            if not all(map(lambda x: x.endswith(".pdf"), name_list)):
                for file in name_list:
                    os.remove(file)
                return render_template('Merger.html', message = "Please upload PDF files only")

            if any(map(lambda x: PdfFileReader(x).isEncrypted, name_list)):
                for file in name_list:
                    os.remove(file)
                return render_template('Merger.html', 
                            message = "Some of the uploaded files are encrypted")


            return render_template('Merger.html', message = "",
                            actual_name_list = actual_name_list, name_list = name_list)
        except:
            return render_template('Merger.html', message = "Some error occured. Please try again")


@app.route('/merger', methods = ['POST'])
def merger():
    try:
        name_list = request.get_json()["ordered_names"]
        output_pdf = PdfFileWriter()
        for file in name_list:
            input_pdf = PdfFileReader(file)
            total_pages = input_pdf.getNumPages()
            for page in range(total_pages):
                output_pdf.addPage(input_pdf.getPage(page))

        date_time = datetime.now().strftime("%d%m%Y%H%M%S")
        with open(f'merged_{date_time}.pdf', "wb") as writefile:
            output_pdf.write(writefile)
        
        for file in name_list:
            os.remove(file)

        return_data = io.BytesIO()
        with open(f'merged_{date_time}.pdf', 'rb') as fo:
            return_data.write(fo.read())
        return_data.seek(0)

        os.remove(f'merged_{date_time}.pdf')

        return send_file(return_data, mimetype = 'application/pdf',
                        attachment_filename = f'merged_{date_time}.pdf')
    except:
        return render_template('Merger.html', message = "Some error occured. Please try again")

if __name__ == '__main__':
    app.run(debug = True)