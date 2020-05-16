# import Flask and other dependencies
import datetime as dt
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///hawaii.sqlite")
# Reflect an existing database into a new model
Base = automap_base()
# Reflect the tables
Base.prepare(engine, reflect=True)
# Save references to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
# Create an app, being sure to pass __name__
app = Flask(__name__)

@app.route("/")
# Define what to do when a user hits the index route
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

@app.route("/api/v1.0/precipitation")
# Define what to do when a user hits the precipitation route
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-23").order_by(Measurement.date).all()
    session.close()
    # Create a dictionary from the row data and append to a list
    query_converted_to_dict = []
    for date, prcp in results:
        precipitation_dictionary = {}
        precipitation_dictionary["Date"] = date
        precipitation_dictionary["Precipitation"] = prcp
        query_converted_to_dict.append(precipitation_dictionary)
    return jsonify(query_converted_to_dict)

@app.route("/api/v1.0/stations")
# Define what to do when a user hits the stations route
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()
    # Convert list of tuples into normal list
    stations = list(np.ravel(results))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
# Define what to do when a user hits the tobs route
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= "2016-08-18").\
        filter(Measurement.station == 'USC00519281').order_by(Measurement.date).all()
    session.close()
    # Create a dictionary from the row data and append to a list
    query_converted_to_dict = []
    for date, tobs in results:
        tobs_dictionary = {}
        tobs_dictionary["Date"] = date
        tobs_dictionary["Temperature Observed"] = tobs
        query_converted_to_dict.append(tobs_dictionary)
    return jsonify(query_converted_to_dict)

@app.route("/api/v1.0/<start>")
# Define what to do when a user hits the start date route
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs),\
         func.avg(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.date).all()
    session.close()
    # Create a dictionary from the row data and append to a list
    date = dt.datetime.strptime(start, "%Y-%m-%d")
    query_converted_to_dict = []
    for date, min, avg, max in results:
        start_dictionary = {}
        start_dictionary["Date"] = date
        start_dictionary["TMIN"] = min
        start_dictionary["TAVG"] = avg
        start_dictionary["TMAX"] = max
        query_converted_to_dict.append(start_dictionary)
    return jsonify(query_converted_to_dict)

@app.route("/api/v1.0/<start>/<end>")
# Define what to do when a user hits the start/end dates route
def start_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start, Measurement.date <= end).group_by(Measurement.date).all()
    session.close()
    # Create a dictionary from the row data and append to a list 
    query_converted_to_dict = []
    date = dt.datetime.strptime(start, "%Y-%m-%d")
    for date, min, avg, max in results:
        startend_dictionary = {}
        startend_dictionary["Date"] = date
        startend_dictionary["TMIN"] = min
        startend_dictionary["TAVG"] = avg
        startend_dictionary["TMAX"] = max
        query_converted_to_dict.append(startend_dictionary)
    return jsonify(query_converted_to_dict)

# Define main behavior
if __name__ == "__main__":
    app.run(debug=True)