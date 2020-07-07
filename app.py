import datetime as dt
import numpy as np
import pandas as pd
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#get access and query the SQLite database
engine = create_engine("sqlite:///hawaii.sqlite")
Base= automap_base()
Base.prepare(engine, reflect= True)
#Save our references to each table 
Measurement= Base.classes.measurement
Station= Base.classes.station
#create a session link from Python to our database
session = Session(engine)

app= Flask(__name__)

@app.route("/")
def welcome():
    return (
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
    #create dictionary like case for the information downloaded
    precip= {date: prcp for date, prcp in precipitation}
    return jsonify(precip)


@app.route("/api/v1.0/stations")
def stations():
    #query to get all the stations
    results = session.query(Station.station).all()
    stations= list(np.ravel(results))
    return jsonify(stations= stations)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]           

    if not end:
        results = session.query(*sel).filter(Measurement.date <= start).all()
        temps = list(np.ravel(results))
        
        return jsonify(temps= temps)

    results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

@app.route("/api/v1.0/tobs")
def temp_montnly():
    prev_year= dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    
    temps= list(np.ravel(results))
    return jsonify(temps=temps)