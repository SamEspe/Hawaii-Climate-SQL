# Import dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create app
app = Flask(__name__)

# Routes

# Homepage
@app.route('/')
def homepage():
    print("Homepage requested")
    return("Welcome to Sam's Climate App. <br/> Here are the available routes: <br/>")

# Precipitation

@app.route('/api/v1.0/precipitation')
def precipitation:


# Stations

@app.route('/api/v1.0/stations')
def stations:

# Temperature Observations
@app.route('/api/v1.0/tobs')

# Temperature - all dates after "start"
@app.route('/api/v1.0/<start>')

# Temperature - date range
@app.route('/api/v1.0/<start>/<end>')

# Run Flask server
if __name__ == "__main__":
    app.run(debug=True)
