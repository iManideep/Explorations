from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/whatsappapi", methods=['POST'])
def sms_reply():
    input = request.form.get('Body')
    response=requests.get("https://api.covid19india.org/state_district_wise.json").json()
    str_converter=lambda state_name: "".join(state_name.lower().split())
    
    if str_converter(input) in list(map(str_converter,list(response))):
        state_name=list(response)[list(map(str_converter,list(response))).index(str_converter(input))]
        state_details=response[state_name]['districtData']
        active_cases=sum(district['active'] for district in state_details.values())
        confirmed_cases=sum(district['confirmed'] for district in state_details.values())
        deceased_cases=sum(district['deceased'] for district in state_details.values())
        recovered_cases=sum(district['recovered'] for district in state_details.values())
    else:
        for district in response.values():
            district_lists=list(district['districtData'].keys())
            if str_converter(input) in list(map(str_converter,district_lists)):
                district_name=district_lists[list(map(str_converter,district_lists)).index(str_converter(input))]
                active_cases=district['districtData'][district_name]['active']
                confirmed_cases=district['districtData'][district_name]['confirmed']
                deceased_cases=district['districtData'][district_name]['deceased']
                recovered_cases=district['districtData'][district_name]['recovered']
    try:
        active_cases
    except:
        update_string="Invalid Input! Please Enter a valid State/District Name"
    else:
        update_string="No.of Active Cases:{a}\nNo.of Confirmed Cases:{b}\nNo.of Deceased:{c}\nNo.of Recovered:{d}".format(a=active_cases,b=confirmed_cases,c=deceased_cases,d=recovered_cases)
    
    resp = MessagingResponse()
    resp.message(update_string)

    return str(resp)

if __name__ == "__main__":
    app.run()