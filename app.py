from flask import Flask, render_template, request, jsonify
import os
import sqlite3
import json
from datetime import datetime, timedelta

app = Flask(__name__, static_folder="static", template_folder="templates")

# City name to IATA mapping
city_to_iata = {
    "Mumbai": "BOM",
    "Goa": "GOI",
    "Delhi": "DEL",
    "Bangalore": "BLR",
    "Kanpur": "KNU",
    "Guwahati": "GAU",
    "Vishakhapatnam": "VTZ",
    "Jammu": "IXJ",
    "Bihar": "PAT",
    "LA": "LAX",
    "Chicago": "ORD",
    "Madrid": "MAD",
    "Barcelona": "BCN",
    "Dubai": "DXB"
}

# Create necessary directories
def create_directories():
    os.makedirs(os.path.join(app.static_folder, 'css'), exist_ok=True)
    os.makedirs(os.path.join(app.static_folder, 'js'), exist_ok=True)
    os.makedirs(os.path.join(app.static_folder, 'images'), exist_ok=True)

create_directories()

# Initialize SQLite DB with fallback data
def init_db():
    conn = sqlite3.connect('flights.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS flights
                 (id TEXT PRIMARY KEY,
                  airline TEXT,
                  flight_number TEXT,
                  origin TEXT,
                  destination TEXT,
                  departure_time TEXT,
                  arrival_time TEXT,
                  price REAL,
                  seats_available INTEGER,
                  class TEXT)''')
    c.execute("SELECT COUNT(*) FROM flights")
    if c.fetchone()[0] == 0:
        sample_flights = [
            ('FL001', 'Delta Airlines', 'DL123', 'JFK', 'LAX', '2025-04-12T08:00:00', '2025-04-12T11:30:00', 400, 120, 'Economy'),
            ('FL002', 'United Airlines', 'UA456', 'LAX', 'JFK', '2025-04-12T14:00:00', '2025-04-12T22:30:00', 349.99, 85, 'Business')
        ]
        c.executemany('INSERT INTO flights VALUES (?,?,?,?,?,?,?,?,?,?)', sample_flights)
    conn.commit()
    conn.close()

init_db()

# Serve basic pages
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/blog1")
def blog1():
    return render_template("blog1.html")

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

# Flight Search API
@app.route("/search_flights", methods=["GET"])
def search_flights():
    origin = request.args.get("origin", "").strip()
    destination = request.args.get("destination", "").strip()
    date = request.args.get("date", "2025-04-12")

    origin_code = city_to_iata.get(origin, origin)
    destination_code = city_to_iata.get(destination, destination)

    flights = []

    try:
        with open('flights.json', 'r') as f:
            flights_data = json.load(f)  # No .get, just load list
            for flight in flights_data:
                if flight['origin'].lower() == origin_code.lower() and flight['destination'].lower() == destination_code.lower():
                    updated_flight = flight.copy()
                    updated_flight['departureTime'] = f"{date} 10:00:00"
                    updated_flight['arrivalTime'] = f"{date} 13:00:00"
                    flights.append(updated_flight)

        if flights:
            return jsonify(flights)

    except Exception as e:
        print(f"Error reading flights.json: {e}")

    # Fallback to SQLite
    conn = sqlite3.connect('flights.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM flights WHERE origin = ? AND destination = ?''',
              (origin_code, destination_code))

    for row in c.fetchall():
        flights.append({
            'id': row[0],
            'airline': row[1],
            'flightNumber': row[2],
            'origin': row[3],
            'destination': row[4],
            'departureTime': f"{date} 10:00:00",
            'arrivalTime': f"{date} 13:00:00",
            'price': row[7],
            'seatsAvailable': row[8],
            'class': row[9]
        })
    conn.close()

    if not flights:
        print(f"No flights found for: {origin_code} to {destination_code}")

    return jsonify(flights)



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

