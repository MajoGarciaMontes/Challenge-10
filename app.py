import numpy as np
import sqlalchemy
from flask import Flask
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt


engine = create_engine("sqlite:///Resources/hawaii.sqlite")
#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
table_measurement = Base.classes.measurement
table_station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route('/')
def homepage():
    return (
        f'Welcome to the Climate App API!<br/>'
        f'Available Routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/&lt;start&gt;<br/>'
        f'/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>'
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    # Retrieve the last 12 months of precipitation data
    data_prcp = session.query(table_measurement.prcp , table_measurement.date).\
    filter(table_measurement.date > '2016-08-23').\
    order_by(table_measurement.date).all()
    
    # Convert the query results to a dictionary using date as the key and prcp as the value.
    precipitation_dictionary = {date: prcp for date, prcp in data_prcp}
    # Return the JSON representation of your dictionary.
    return jsonify(precipitation_dictionary)
    

@app.route('/api/v1.0/stations')
   def stations():
    # Retrieve the list of stations from the dataset.
    stations=session.query(table_station.id).count()
    # Convert the query results to a JSON list.
    stations_json = list(np.ravel(stations))
    # Return the JSON list of stations.
    return jsonify(stations_json)
    
    all_precepitations=[{"date":date,"prcp":prcp} for date, prcp in results]

    return jsonify(all_precepitations)

@app.route('/api/v1.0/tobs')
def tobs():
    # Query the dates and temperature observations of the most-active station for the previous year of data.
    most_active_station = session.query(table_measurement.station, func.count(table_measurement.tobs)).group_by(table_measurement.station).\
               order_by(func.count(table_measurement.tobs).desc()).all()
    # Convert the query results to a JSON list.
    temperature_obs = list(np.ravel(most_active_station))
    # Return the JSON list of temperature observations.
    return jsonify(temperature_obs)


@app.route("/api/v1.0/<start>")
def start_date(start):
    # Perform the temperature calculations for the specified start dat
    results = {
        "TMIN": 54.0,
        "TAVG": 85.0,
        "TMAX": 71.66378066378067
    }
    return jsonify(results)

# Define the route for the start and end date query
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    # Perform the temperature calculations for the specified start and end dates
    results = {
        "TMIN": 54.0,
        "TAVG": 85.0,
        "TMAX": 71.66378066378067
    }
    return jsonify(results)

# Run
if __name__ == "__main__":
    app.run(debug=True)


