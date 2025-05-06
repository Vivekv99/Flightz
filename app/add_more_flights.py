import sqlite3
import random
from datetime import datetime, timedelta

# List of extra airlines to choose from
extra_airlines = ["Air India", "IndiGo", "SpiceJet", "Go First", "Vistara", "Akasa Air", "Jet Airways"]
flight_classes = ["Economy", "Business", "Premium Economy"]

def get_random_airline(existing_airlines):
    available = [a for a in extra_airlines if a not in existing_airlines]
    return random.choice(available) if available else random.choice(extra_airlines)

def generate_flight_number():
    prefix = ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=2))
    number = random.randint(100, 999)
    return f"{prefix}{number}"

def get_next_flight_id(cursor):
    cursor.execute("SELECT id FROM flights")
    ids = cursor.fetchall()
    max_id_num = 0
    for id_row in ids:
        id_str = id_row[0].replace("FL", "")
        if id_str.isdigit():
            max_id_num = max(max_id_num, int(id_str))
    return max_id_num + 1

def insert_additional_flights():
    conn = sqlite3.connect('flights.db')
    c = conn.cursor()

    # Step 1: Fetch all existing route pairs
    c.execute("SELECT origin, destination, airline FROM flights")
    rows = c.fetchall()

    route_map = {}
    for origin, destination, airline in rows:
        key = (origin, destination)
        if key not in route_map:
            route_map[key] = []
        route_map[key].append(airline)

    # Step 2: Start from next available flight ID
    next_id = get_next_flight_id(c)

    for (origin, destination), airlines in route_map.items():
        needed = 3 - len(airlines)
        for _ in range(needed):
            airline = get_random_airline(airlines)
            airlines.append(airline)
            flight_number = generate_flight_number()
            departure_time = datetime(2025, 4, 14, random.randint(0, 23), random.choice([0, 15, 30, 45]))
            arrival_time = departure_time + timedelta(hours=random.randint(2, 6))
            price = random.randint(3000, 8000)
            seats = random.randint(50, 150)
            seat_class = random.choice(flight_classes)

            flight_id_str = f"FL{next_id}"
            next_id += 1

            c.execute('''
                INSERT INTO flights (id, airline, flight_number, origin, destination,
                                     departure_time, arrival_time, price, seats_available, class)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (flight_id_str, airline, flight_number, origin, destination,
                  departure_time.isoformat(), arrival_time.isoformat(), price, seats, seat_class))

    conn.commit()
    conn.close()
    print("✅ Additional flights inserted successfully!")

if __name__ == "__main__":
    insert_additional_flights()
