import os
import pickle
from flask import Flask,request,jsonify,render_template
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

application=Flask(__name__)
app=application

# Get the directory of the current file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load models using absolute paths
ridge_model = pickle.load(open(os.path.join(BASE_DIR, 'models', 'ridge.pkl'), 'rb'))
standard_scaler = pickle.load(open(os.path.join(BASE_DIR, 'models', 'scaler.pkl'), 'rb'))

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/predictdata',methods=['GET','POST'])
def predict_datapoint():
    if request.method=='POST':
        Temperature=float(request.form.get('Temperature'))
        RH=float(request.form.get('RH'))
        Ws=float(request.form.get('Ws'))
        Rain=float(request.form.get('Rain'))
        FFMC=float(request.form.get('FFMC'))
        DMC=float(request.form.get('DMC'))
        ISI=float(request.form.get('ISI'))
        Classes=float(request.form.get('Classes'))
        Region=float(request.form.get('Region'))

        new_data_scaler=standard_scaler.transform([[Temperature,RH,Ws,Rain,FFMC,DMC,ISI,Classes,Region]])
        result=ridge_model.predict(new_data_scaler)

        return render_template('home.html',result=result[0])

    else:
        return render_template('home.html')
    

if __name__=="__main__":
    app.run(host="0.0.0.0")