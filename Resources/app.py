# 1. import Flask
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def percipitation():
# Create our session (link) from Python to the DB
    session = Session(engine)
# Select only the `date` and `prcp` values.
# Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

 # Create a dictionary from the row data and append to a list of all
    precipitation_data = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation_data.append(precipitation_dict)

    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def station():
# Create our session (link) from Python to the DB
    session = Session(engine)
#Return a JSON list of stations from the dataset.
    results = session.query(Station.name, Station.station).all()
    session.close()
   

# Create a dictionary from the row data and append to a list of all
    station_data = []
    for data in results:
        station_dict = {}
        station_dict["name"] = data[0]
        station_dict["station"] = data[1]
        station_data.append(station_dict)

    return jsonify(station_data)

@app.route("/api/v1.0/tobs")
def tobs():
# Create our session (link) from Python to the DB
    session = Session(engine)
#query for the dates and temperature observations from a year from the last data point.
#Return a JSON list of Temperature Observations (tobs) for the previous year.

    Latest_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    Latest_date = session.query(func.max(Measurement.date)).scalar()
    Latest_date = dt.datetime.strptime(Latest_date, '%Y-%m-%d')
    lastyear_date = Latest_date - dt.timedelta(days=365)
    results =session.query(Measurement.tobs).filter(Measurement.date > lastyear_date).all()
    session.close()

    tobs_data = []
    for data in results:
        tobs_dict = {}
        tobs_dict["tobs"] = data[0]
        tobs_data.append(tobs_dict)

    return jsonify(tobs_data)

@app.route("/api/v1.0/start")
def start():
    #start_date = 11/12/2015
    
# Create our session (link) from Python to the DB
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
        filter(Measurement.date >= '2017-08-10').group_by(Measurement.date).all()
    session.close()

    start_data = []
    for data in results:
        start_dict = {}
        start_dict['tmin'] = data[0]
        start_dict['tmax'] = data[1]
        start_dict['tavg'] = data[2]
        start_data.append(start_dict)

    return jsonify(start_data)

@app.route("/api/v1.0/start/end")
def start_end():
    # Create our session (link) from Python to the DB
    start_date = '2017-08-07'
    end_date = '2017-08-10'

    session = Session(engine)
    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
        filter(Measurement.date>=start_date).filter(Measurement.date<=end_date).group_by(Measurement.date).all()
    session.close()

    end_data = []
    for data in results:
        end_dict = {}
        end_dict['tmin'] = data[0]
        end_dict['tmax'] = data[1]
        end_dict['tavg'] = data[2]
        end_data.append(end_dict)

    return jsonify(end_data)

if __name__ == "__main__":
    app.run(debug=True)