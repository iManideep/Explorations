import random
from flask import Flask,request,redirect,render_template
import pickle

test_dict=dict()
with open("database.pkl","wb") as f:
    pickle.dump(test_dict,f)

app=Flask(__name__)
DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',  
                     'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q', 
                     'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 
                     'z']
UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',  
                     'I', 'J', 'K', 'M', 'N', 'O', 'p', 'Q', 
                     'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 
                     'Z']
COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS

@app.route("/create_id",methods=["POST"])
def create_id():
    actual_url=request.form["inputurl"]
    temp_pass=""
    temp_pass += random.choice(DIGITS)
    temp_pass += random.choice(UPCASE_CHARACTERS) 
    temp_pass += random.choice(LOCASE_CHARACTERS)
    for _ in range(3):
        temp_pass += random.choice(COMBINED_LIST)
    temp_pass_list=temp_pass.split()
    random.shuffle(temp_pass_list)
    shortened_id="".join(temp_pass_list)
    with open("database.pkl","rb") as f:
        loaded_data=pickle.load(f)
    loaded_data[shortened_id]=actual_url
    with open("database.pkl","wb") as f:
        pickle.dump(loaded_data,f)
    return render_template("index.html",home=False,short_link=f"/{shortened_id}",URL=f"https://localhost:5000/{shortened_id}")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def redirecter(path):
    if path.replace(" ","") == '':
        return render_template("index.html",home=True)
    else:
        with open("database.pkl","rb") as f:
            loaded_data=pickle.load(f)
        actual_url=loaded_data[path]
        return redirect(actual_url)
app.run(debug=True)