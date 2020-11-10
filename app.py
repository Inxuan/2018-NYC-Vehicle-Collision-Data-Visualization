import json
import random
from sklearn import cluster, datasets
from flask import Flask, render_template, request, redirect, Response, jsonify
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import MDS
import numpy as np

import math

app = Flask(__name__,static_url_path='/static')

global borough
global latitude
global longitude
global date
global time

global longitude2
global latitude2
global points2

global longitude3
global latitude3
global points3

global longitude4
global latitude4
global points4

global injure

global rainy
global foggy

global hour
global kill
global month
global weather
@app.route("/", methods = ['POST', 'GET'])
def home():


    return render_template("home.html", borough=borough,latitude=latitude,longitude=longitude,date=date,time=time,hour= hour,month=month,
                         longitude2=longitude2,latitude2=latitude2,points2=points2,
                           longitude3=longitude3, latitude3=latitude3, points3=points3,
                           longitude4=longitude4, latitude4=latitude4, points4=points4,injure=injure,kill=kill,weather=weather)

def zoom(xmin,xmax,ymin,ymax,factor):
    temp=[]
    for i in range(0,factor*factor):
        temp.append([])
    for i in range(0,len(longitude)):
        temp[math.floor((longitude[i]-xmin)/((xmax-xmin)/factor))+math.floor((latitude[i]-ymin)/((ymax-ymin)/factor))*factor].append(i)
    return temp

def getCenterX(p):
    temp=[]
    for i in range(0,len(p)):
        if(len(p[i])==0):
            temp.append(0)
        else:
            count=0
            sum=0
            for e in p[i]:
                count+=1
                sum+=longitude[e]
            temp.append(sum/count)
    return temp

def getCenterY(p):
    temp=[]
    for i in range(0,len(p)):
        if(len(p[i])==0):
            temp.append(0)
        else:
            count=0
            sum=0
            for e in p[i]:
                count+=1
                sum+=latitude[e]
            temp.append(sum/count)
    return temp

if __name__ == "__main__":

    df1 = pd.read_csv('NYPD_Motor_Vehicle_Collisions.csv')
    db=df1.sample(frac=0.07, replace=True, random_state=1)
    borough=db["BOROUGH"].tolist()
    latitude = db["LATITUDE"].tolist()
    longitude = db["LONGITUDE"].tolist()
    date = db["DATE"].tolist()
    time = db["TIME"].tolist()

    injure1 = db["NUMBER OF PERSONS INJURED"].tolist()
    injure2 = db["NUMBER OF PERSONS KILLED"].tolist()
    injure3 = db["NUMBER OF PEDESTRIANS INJURED"].tolist()
    injure4 = db["NUMBER OF PEDESTRIANS KILLED"].tolist()
    injure5 = db["NUMBER OF CYCLIST INJURED"].tolist()
    injure6 = db["NUMBER OF CYCLIST KILLED"].tolist()
    injure7 = db["NUMBER OF MOTORIST INJURED"].tolist()
    injure8 = db["NUMBER OF MOTORIST KILLED"].tolist()

    injure=[]
    for i in range(0,len(injure1)):
        injure.append(int(injure1[i]+injure2[i]))

    kill=injure2
    xmax = -73.582201
    xmin = -74.269729
    ymax = 40.924259
    ymin = 40.478081

    points2=zoom(xmin,xmax,ymin,ymax,40)
    longitude2=getCenterX(points2)
    latitude2 = getCenterY(points2)

    points3 = zoom(xmin, xmax, ymin, ymax, 30)
    longitude3 = getCenterX(points3)
    latitude3 = getCenterY(points3)

    points4 = zoom(xmin, xmax, ymin, ymax, 20)
    longitude4 = getCenterX(points4)
    latitude4 = getCenterY(points4)

    weatherdb = pd.read_csv('Weather.csv')
    date2 = weatherdb["DATE"].tolist()
    wea=weatherdb["CONDITION"].tolist()


    weather=[]
    for i in range(0,len(longitude)):
        w=wea[date2.index(date[i])]
        if w=="rainy":
            weather.append(1)
        elif w=="foggy":
            weather.append(3)
        elif w=="snow":
            weather.append(2)
        else:
            weather.append(0)
    hour=[]
    for e in time:
        temp = (int)(e.split(":")[0])
        temp = math.floor(temp / 2)
        hour.append(temp)
    month=[]
    for e in date:
        month.append(e.split("/")[0])




    app.run(debug=True)
