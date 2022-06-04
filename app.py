import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func 

import flask
from flask import Flask, jsonify


#set up database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#reflect tables 
Base = automap_base()
Base.prepare(engine, reflect=True)

#save classes to variable
Measurement = Base.classes.measurement
Station = Base.classes.station

#Create link to database
session = Session(engine)

#set up flask
app = Flask(__name__)

#Create the routes
@app.route("/")
def welcome():
    return(
    f"Welcome to the Climate Analysis API!</br>"
    f"Available Routes:</br>"
    f"/api/v1.0/precipitation</br>"
    f"/api/v1.0/stations</br>"
    f"/api/v1.0/tobs</br>"
    f"/api/v1.0/temp/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
    
    
    precip = {
        date: prcp for date, prcp in precipitation
    }
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
def tobs():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
    

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None,end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end:
        results = session.query(*sel).filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)
    
    results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)
    

if __name__ == "__main__":
    app.run(debug=True)