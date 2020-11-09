import json
import random

from flask import Flask, render_template, request, redirect, Response, jsonify
import pandas as pd
import numpy as np
#First of all you have to import it from the flask module:
app = Flask(__name__,static_url_path='/static')
#By default, a route only answers to GET requests. You can use the methods argument of the route() decorator to handle different HTTP methods.

@app.route("/", methods = ['POST', 'GET'])
def home():
    global borough
    global latitude
    global longitude
    global date
    global time
    return render_template("home.html", borough=borough,latitude=latitude,longitude=longitude,date=date,time=time)

if __name__ == "__main__":

    df1 = pd.read_csv('NYPD_Motor_Vehicle_Collisions.csv')
    db=df1.sample(frac=0.07, replace=True, random_state=1)
    borough=db["BOROUGH"].tolist()
    latitude = db["LATITUDE"].tolist()
    longitude = db["LONGITUDE"].tolist()
    date = db["DATE"].tolist()
    time = db["TIME"].tolist()

    app.run(debug=True)
