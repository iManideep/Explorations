# https://blog.alivate.com.au/poppler-windows/
from flask import Flask, render_template, request, send_file
from pdf2image import convert_from_path
from werkzeug.utils import secure_filename
import os
import io
from PyPDF2 import PdfFileWriter, PdfFileReader
app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('Sorter.html', message = "")
    elif request.method == 'POST':
        try:
            for file in os.listdir():
                if file.endswith(".pdf"):
                    os.remove(file)
            images_path = os.path.abspath(__file__+r"\..\static\images")
            for file in os.listdir(images_path):
                if file.endswith(".jpg"):
                    os.remove(images_path+"/"+file)

            f = request.files['file']
            if f.filename.replace(" ","") == "":
                return render_template('Sorter.html', 
                            message = "Please upload PDF file before submitting")
            
            f.save(secure_filename(f.filename))
            fileName = f.filename.replace(" ","_").replace("(","").replace(")","")
            if not fileName.endswith(".pdf"):
                os.remove(fileName)
                return render_template('Sorter.html', message = "Please upload PDF file only")
            
            input_pdf = PdfFileReader(fileName)
            if input_pdf.isEncrypted:
                return render_template('Sorter.html', message = "Please upload PDF without encryption only")
            
            poppler_path = os.path.abspath(__file__+r"\..\..\..\..\..\Downloads\poppler-0.68.0_x86\poppler-0.68.0\bin")
            images = convert_from_path(fileName,500, poppler_path = poppler_path)
            images_list = []
            for idx,img in enumerate(images):
                name = f"{str(idx)}.jpg"
                images_list.append(name)
                img.save(images_path+"/"+name,"JPEG")

            return render_template('Sorter.html', message = "",
                            images_list = images_list)
        except:
            return render_template('Sorter.html', message = "Some error occured. Please try again")


@app.route('/sorter', methods = ['POST'])
def sorter():
    try:
        images_order = request.get_json()["ordered_images"]
        images_order = list(map(int,images_order))
        images_path = os.path.abspath(__file__+r"\..\static\images")
        for file in os.listdir(images_path):
            if file.endswith(".jpg"):
                os.remove(images_path+"/"+file)
        for file in os.listdir():
            if file.endswith(".pdf"):
                fileName = file
                break
        input_pdf = PdfFileReader(fileName)
        total_pages = input_pdf.getNumPages()

        if sorted(images_order) != list(range(total_pages)):
            return render_template('Sorter.html', message = "Images on HTML are tampered")
        
        output_pdf = PdfFileWriter()
        for page_number in images_order:
            output_pdf.addPage(input_pdf.getPage(page_number))

        with open(f'reordered_{fileName}', "wb") as writefile:
            output_pdf.write(writefile)
        
        os.remove(fileName)

        return_data = io.BytesIO()
        with open(f'reordered_{fileName}', 'rb') as fo:
            return_data.write(fo.read())
        return_data.seek(0)

        os.remove(f'reordered_{fileName}')

        return send_file(return_data, mimetype = 'application/pdf',
                        attachment_filename = f'reordered_{fileName}')
    except:
        return render_template('Sorter.html', message = "Some error occured. Please try again")

if __name__ == '__main__':
    app.run(debug = True)