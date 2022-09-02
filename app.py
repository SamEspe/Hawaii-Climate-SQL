# Import dependencies
from calendar import day_abbr
import json
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create Flask app
app = Flask(__name__)

# Create Flask Routes

# Homepage
@app.route('/')
def homepage():
    print("Homepage requested")
    return("Welcome to Sam's Climate App. <br/> \
    Here are the available routes: <br/> <br/>\
    /api/v1.0/precipitation <br/> \
    /api/v1.0/stations <br/> \
    /api/v1.0/tobs <br/> \
    /api/v1.0/search")

# Precipitation
@app.route('/api/v1.0/precipitation')
def precipitation():
    # Open session
    session = Session(engine)

    # Query for precipitation data (like in Jupyter Notebook)
    last_date = session.query(func.max(Measurement.date)).first()[0]
    last_date_dt = dt.datetime.strptime(last_date, '%Y-%m-%d')
    year_ago = last_date_dt - dt.timedelta(days = 366)
    year_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).filter(Measurement.date <= last_date).all()

    # Close session
    session.close()

    # Make query results into a dictionary with keys being dates and values being prcp
    all_prcp_data = []
    for date, prcp in year_data:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp_data.append(prcp_dict)

    # Return jsonified dictionary
    return jsonify(all_prcp_data)

# Stations
@app.route('/api/v1.0/stations')
def stations():
    # Open session
    session = Session(engine)

    # Query for station data (like in JN)
    stations_raw = session.query(Station.station, Station.name).all()

    # Close session
    session.close()

    # Make query results into JSON list
    stations = []
    for station, name in stations_raw:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        stations.append(station_dict)
    
    return jsonify(stations)

# Temperature Observations
@app.route('/api/v1.0/tobs')
def tobs():
    # Open session
    session = Session(engine)

    # Query for tobs data (like in JN)
    last_date2 = session.query(func.max(Measurement.date)).filter(Measurement.station == "USC00519281").first()[0]
    last_date2_dt = dt.datetime.strptime(last_date2, '%Y-%m-%d')
    year_ago2 = last_date2_dt - dt.timedelta(days = 365)

    temp_data_year = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == "USC00519281").filter(Measurement.date >= year_ago2).filter(Measurement.date <= last_date2).all()
    # Close session
    session.close()

    # Make dictionary
    temp_data = []

    for date, tobs in temp_data_year:
        date_tobs = {}
        date_tobs["date"] = date
        date_tobs["tobs"] = tobs
        temp_data.append(date_tobs)

    # Return JSONified version
    return jsonify(temp_data)

# Temperature - all dates after "start"
# @app.route('/api/v1.0/<start>')

# Temperature - date range
# @app.route('/api/v1.0/<start>/<end>')

# Run Flask server
if __name__ == '__main__':
    app.run(debug=True)
