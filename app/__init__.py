from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import requests, json
import os
from os import environ

#Variables:
miUser = os.environ["MIUSER"]
miPass = os.environ["MIPASS"]


from urllib.request import urlopen
tortmapjsonURL = os.environ["TORTMAPURL"]
data = urlopen(tortmapjsonURL).read(20000).decode('utf-8')
data = data.split("\n")
data = str(data)
jsonmap = open("tort2devicemap.json", "a", 1)
jsonmap.write(data)
jsonmap.close()


file =  "tort2devicemap.json"
with open(file) as myfile:
    tortMap = (list(myfile)[-1])

tortListNames = json.loads(tortMap)
tortListNames = tortListNames.keys()

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27d123441f2b6176a'

class ReusableForm(Form):
    switch = TextField('Switch:', validators=[validators.required(), validators.Length(min=3, max=35)])
    state = TextField('State:', validators=[validators.required(), validators.Length(min=2, max=6)])
 
@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)
 
    print (form.errors)
    if request.method == 'POST':
        switch=request.form['switch']
        state=request.form['state']
 
        if form.validate():
            tortKey = switch
            plugId = json.loads(tortMap)[tortKey][0]
            plugSocket = json.loads(tortMap)[tortKey][1]
                        
            if plugId != "":
                plugId = int(plugId)
                if plugSocket == "":
                    plugSocket=None
                    values = {'id' : plugId}
                else:
                    plugSocket=int(plugSocket)
                    values = {'id' : plugId, 'socket' : plugSocket}
                headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
                
                if state == "On":
                    url = "https://mihome4u.co.uk/api/v1/subdevices/power_on"
                else:
                    url = "https://mihome4u.co.uk/api/v1/subdevices/power_off"
            
                try:
                #    r = requests.post(url, data=json.dumps(values), headers=headers, auth=(miUser, miPass))
                    flash(switch + ' light ' + state + '...' + url + json.dumps(values))
                except requests.exceptions.RequestException as e:
                    flash(e)
        else:
            flash('Error: All the form fields are required. ')
 
    return render_template('page.html', form=form, tortListNames=tortListNames)
 
if __name__ == "__main__":
    app.run(host='0.0.0.0')
