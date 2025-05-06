import sqlite3
from datetime import datetime, timedelta

# Connect to the database
conn = sqlite3.connect('flights.db')
c = conn.cursor()

# Cities to create combinations for
cities = [
    "GOA", "NASHIK", "PUNE", "MUMBAI", "DELHI", "BANGLORE",
    "NYC", "LA", "RM", "BARCA"
]

# Sample airlines based on cities
airlines_map = {
    "GOA": ["Goa Express", "IndiGo Goa", "FlyGoa"],
    "MUMBAI": ["Mumbai Air", "JetMumbai", "IndiGo Mumbai"],
    "NASHIK": ["Nashik Airways", "Spice Nashik", "FlyNasik"]
}

default_airline = "Global Airlines"

flight_class = ["Economy", "Business", "Premium Economy"]

# Start date
start_date = datetime(2025, 4, 14, 6, 0)

# Generate flight records
flight_data = []
flight_id = 1000

for i in range(len(cities)):
    for j in range(len(cities)):
        if i != j:
            origin = cities[i]
            destination = cities[j]
            base_time = start_date + timedelta(hours=(i + j) % 12 * 2)
            arrival_time = base_time + timedelta(hours=2)

            # Choose airline
            if origin in airlines_map:
                airline = airlines_map[origin][flight_id % 3]
            else:
                airline = default_airline

            flight = (
                f"FL{flight_id}",
                airline,
                f"{airline[:2].upper()}{flight_id % 1000}",
                origin,
                destination,
                base_time.isoformat(),
                arrival_time.isoformat(),
                round(3000 + (flight_id % 50) * 100, 2),  # Price in INR
                100 + flight_id % 50,
                flight_class[flight_id % 3]
            )
            flight_data.append(flight)
            flight_id += 1

# Insert into database
c.executemany('''
    INSERT OR REPLACE INTO flights 
    (id, airline, flight_number, origin, destination, departure_time, arrival_time, price, seats_available, class) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', flight_data)

conn.commit()
conn.close()

print(f"✅ Inserted {len(flight_data)} flights into flights.db")
