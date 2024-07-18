import json
from datetime import datetime, timedelta
import random
import os
from common.models.base import Base, Train, Station, Platform, Track, Trip
from common.datasources.sqlitedb import SQLiteDataSource

# Ensure the 'data' directory exists
if not os.path.exists('data'):
    os.makedirs('data')

# Load configuration
with open('config/config.json') as f:
    config = json.load(f)

# Set up SQLite database
db_name = f'data/simulation_{datetime.now().strftime("%Y%m%d_%H%M%S")}.sqlite'
data_source = SQLiteDataSource(db_name, Base)
data_source.connect()
session = data_source.get_session()

# Store configuration in the database
for train in config['trains']:
    train_model = Train(train_id=train['train_id'], passenger_capacity=train['passenger_capacity'])
    session.add(train_model)

for station in config['stations']:
    station_model = Station(id=station['id'])
    session.add(station_model)
    session.flush()  # Ensure station ID is available for platforms
    for platform in station['platforms']:
        platform_model = Platform(station_id=station_model.id, passenger_capacity=platform['passenger_capacity'])
        session.add(platform_model)

for track in config['tracks']:
    track_model = Track(
        from_station_id=track['from_station_id'],
        to_station_id=track['to_station_id'],
        direction_code=track['direction_code'],
        average_section_running_time=track['average_section_running_time']
    )
    session.add(track_model)

session.commit()

# Simulation parameters
start_time = datetime.strptime(config['start_time'], '%H:%M')
end_time = datetime.strptime(config['end_time'], '%H:%M')
num_people_per_day = config['num_people_per_day']

# Function to simulate a trip
def simulate_trip(train, origin, destination, srt, trip_start_time):
    num_passengers = random.randint(0, train.passenger_capacity)
    delay = int(num_passengers / train.passenger_capacity * srt)  # Delay based on load
    trip_end_time = trip_start_time + timedelta(minutes=delay + srt)
    trip_model = Trip(
        train_id=train.train_id,
        origin=origin,
        destination=destination,
        length=random.randint(3, 10),
        num_passengers=num_passengers,
        srt=srt,
        start_time=trip_start_time,
        end_time=trip_end_time,
        delay=delay
    )
    session.add(trip_model)
    session.commit()

# Simulate trips
current_time = start_time
while current_time < end_time:
    for train in session.query(Train).all():
        origin = random.choice(session.query(Station).all()).id
        destination = random.choice([s.id for s in session.query(Station).all() if s.id != origin])
        valid_tracks = session.query(Track).filter_by(from_station_id=origin, to_station_id=destination).all()
        if not valid_tracks:
            continue  # Skip if no valid track exists
        srt = random.choice(valid_tracks).average_section_running_time
        simulate_trip(train, origin, destination, srt, current_time)
    current_time += timedelta(minutes=random.randint(5, 15))  # Random interval between trips

# Generate report
trips = session.query(Trip).all()
total_trips = len(trips)
total_passengers = sum(trip.num_passengers for trip in trips)
average_delay = sum(trip.delay for trip in trips) / total_trips if total_trips else 0

print("Simulation Report")
print("=================")
print(f"Total Trips: {total_trips}")
print(f"Total Passengers: {total_passengers}")
print(f"Average Delay: {average_delay:.2f} minutes")
print("\nAll Trips:")
for trip in trips:
    print(trip.to_dict())

# Close session
session.close()
data_source.close()
