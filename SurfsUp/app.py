# Import necessary libraries
from flask import Flask, jsonify
from datetime import datetime  # Add this line
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

# Database setup
engine = create_engine("sqlite:///SurfsUp/Resources/hawaii.sqlite")

# reflect an existing database into a new model
base = automap_base()
base.prepare(engine, reflect=True)

# reflect the tables
measurement = base.classes.measurement
station = base.classes.station

# Create Flask app
app = Flask(__name__)

# Define routes
@app.route("/")
def home():
    return (
        "Welcome to the Climate App API!<br>"
        "Available Routes:<br>"
        "/api/v1.0/precipitation<br>"
        "/api/v1.0/stations<br>"
        "/api/v1.0/tobs<br>"
        "/api/v1.0/start<br>"
        "/api/v1.0/end"
    )

# Define the /api/v1.0/precipitation route
@app.route("/precipitation")
def precipitation():
    # Create a session
    session = Session(engine)

    # Query date and precipitation data
    results = session.query(measurement.date, measurement.prcp).all()

    # Close the session
    session.close()

    # Convert the query results to a dictionary
    precipitation_data = {date: prcp for date, prcp in results}

    # Return the JSON representation of the dictionary
    return jsonify(precipitation_data)

# Define the /api/v1.0/stations route
@app.route("/stations")
def stations():
    # Create a session
    session = Session(engine)

    # Query date and station data
    results = session.query(station.station, station.name).all()

    # Close the session
    session.close()

    # Convert the query results to a dictionary
    station_data = {station: name for station, name in results}

    # Return the JSON representation of the dictionary
    return jsonify(station_data)

# Define the /api/v1.0/tobs route
@app.route("/tobs")
def tobs():
    # Create a session
    session = Session(engine)

    busiest_station = (
        session.query(measurement.station, func.count(measurement.tobs).label("tobs_count"))
        .group_by(measurement.station)
        .order_by(func.count(measurement.tobs).desc())
        .first()
    )

    # Query date, tobs, and station data
    if busiest_station:
        # Extract the station ID of the busiest station
        busiest_station_id = busiest_station[0]

        # Query date, tobs, and station data for the busiest station
        results = (
            session.query(measurement.date, measurement.tobs, measurement.station)
            .filter(measurement.station == busiest_station_id)
            .all()
        )

    # Close the session
    session.close()

    # Convert the query results to a list of dictionaries
    tobs_data = [
        {"date": date, "tobs": tobs, "station": station}
        for date, tobs, station in results
    ]

    # Return the JSON representation of the list of dictionaries
    return jsonify(tobs_data)

# Define the /api/v1.0/start route
@app.route("/start/<start>")
def temperature_stats_start(start):
    # Create a session
    session = Session(engine)

    # Convert the input date string to a datetime object
    start_date = datetime.strptime(start, "%Y-%m-%d")

    # Query TMIN, TAVG, and TMAX for dates greater than or equal to the start date
    results = (
        session.query(
            func.min(measurement.tobs).label("min_temp"),
            func.avg(measurement.tobs).label("avg_temp"),
            func.max(measurement.tobs).label("max_temp"),
        )
        .filter(measurement.date >= start_date)
        .all()
    )

    # Close the session
    session.close()

    # Extract the results and return as JSON
    temperature_stats = {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": None,
        "min_temp": results[0].min_temp,
        "avg_temp": results[0].avg_temp,
        "max_temp": results[0].max_temp,
    }

    return jsonify(temperature_stats)

# Define the /api/v1.0/end route
@app.route("/end/<start>/<end>")
def temperature_stats_start_end(start, end):
    # Create a session
    session = Session(engine)

    # Convert the input date strings to datetime objects
    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")

    # Query TMIN, TAVG, and TMAX for dates between the start and end dates, inclusive
    results = (
        session.query(
            func.min(measurement.tobs).label("min_temp"),
            func.avg(measurement.tobs).label("avg_temp"),
            func.max(measurement.tobs).label("max_temp"),
        )
        .filter(measurement.date.between(start_date, end_date))
        .all()
    )

    # Close the session
    session.close()

    # Extract the results and return as JSON
    temperature_stats = {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "min_temp": results[0].min_temp,
        "avg_temp": results[0].avg_temp,
        "max_temp": results[0].max_temp,
    }

    return jsonify(temperature_stats)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
