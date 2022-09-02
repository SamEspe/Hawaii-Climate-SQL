# Import dependencies
from audioop import avg
from calendar import day_abbr
import json
from re import M
from tkinter import E
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
    <br/> You can also search the records using dates. <br/> \
    - To search from a start date until the last available date, add the date to the URL after /v1.0/ in the form: YYYY-MM-DD <br/> \
    - To search from a start date until an end date, add the start date and end date divided by a slash to the URL after /v1.0/ in the form: YYYY-MM-DD/YYYY-MM-DD")

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
@app.route('/api/v1.0/<start>')
def temps_start(start):
    # Save start date
    start_date = start

    # Open session
    session = Session(engine)

    # Query the database
    min_start_only = session.query(func.min(Measurement.tobs)).filter(Measurement.station == "USC00519281").filter(Measurement.date >= start_date).all()[0][0]
    max_start_only = session.query(func.max(Measurement.tobs)).filter(Measurement.station == "USC00519281").filter(Measurement.date >= start_date).all()[0][0]
    avg_start_only = session.query(func.avg(Measurement.tobs)).filter(Measurement.station == "USC00519281").filter(Measurement.date >= start_date).all()[0][0]

    # Close session
    session.close()

    # Round average to 2 decimal points
    avg_rounded = round(avg_start_only, 2)

    # Create output dictionary
    output_dict = {}
    output_dict["TMIN"] = min_start_only
    output_dict["TMAX"] = max_start_only
    output_dict["TAVG"] = avg_rounded

    # Return query results
        
    return jsonify(output_dict)

# Temperature - date range
@app.route('/api/v1.0/<start>/<end>')
def temps_start_end(start,end):
    # Save start and end dates
    start_date = start
    end_date = end

    # Open session
    session = Session(engine)

    # Query the database
    min_start_end = session.query(func.min(Measurement.tobs)).filter(Measurement.station == "USC00519281").filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()[0][0]
    max_start_end = session.query(func.max(Measurement.tobs)).filter(Measurement.station == "USC00519281").filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()[0][0]
    avg_start_end = session.query(func.avg(Measurement.tobs)).filter(Measurement.station == "USC00519281").filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()[0][0]
    
    # Close session
    session.close()
    # Round average to 2 decimal points

    avg_start_end_rounded = round(avg_start_end, 2)

    # Create output dictionary
    output_dict = {}
    output_dict["TMIN"] = min_start_end
    output_dict["TMAX"] = max_start_end
    output_dict["TAVG"] = avg_start_end_rounded

    # Return query results
    
    return jsonify(output_dict)


# Run Flask server
if __name__ == '__main__':
    app.run(debug=True)
