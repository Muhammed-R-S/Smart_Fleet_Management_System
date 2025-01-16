import asyncio
import sqlite3

# Create a SQLite3 database connection
conn = sqlite3.connect('vehicle_data.db')
cursor = conn.cursor()

# Create tables for each vehicle if they don't exist
vehicles = {
    'vehicleA': {'fuel_level': 80.0, 'speed_level': 0, 'temperature': 25},
    'vehicleB': {'fuel_level': 70.0, 'speed_level': 10, 'temperature': 30},
    'vehicleC': {'fuel_level': 75.0, 'speed_level': 5, 'temperature': 27},
    'vehicleD': {'fuel_level': 78.0, 'speed_level': 7, 'temperature': 20},
}

for vehicle_id, vehicle_data in vehicles.items():
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {vehicle_id} (
                        id INTEGER PRIMARY KEY,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        fuel_level REAL,
                        speed_level INTEGER,
                        temperature INTEGER,
                        fuel_alerts INTEGER
                    )''')
    conn.commit()


async def generate_data():
    # Define increments or decrements for each vehicle
    increments = {
        'fuel_level': -1,  # Decrease fuel level by 0.2 every iteration
        'speed_level': 5,  # Increase speed level by 3 every iteration
        'temperature': 2   # Increase temperature by 1 every iteration
    }

    while True:
        for vehicle_id, vehicle_data in vehicles.items():
            for key, increment in increments.items():
                # Update each value with the defined increment
                vehicle_data[key] += increment

                # Reset values if they go out of bounds
                if key == 'fuel_level':
                    if vehicle_data[key] <= 0:
                        vehicle_data[key] = 80.0
                elif key == 'speed_level':
                    if vehicle_data[key] >= 200:
                        vehicle_data[key] = 0
                elif key == 'temperature':
                    if vehicle_data[key] > 180:
                        vehicle_data[key] = 25

            # Format fuel level to display only two digits after the decimal
            vehicle_data['fuel_level'] = round(vehicle_data['fuel_level'], 2)

            # Check if fuel level is less than 10 and update fuel alerts count
            vehicle_data['fuel_alerts'] = 1 if vehicle_data['fuel_level'] < 15.0 else 0

            # Insert data into the respective vehicle's table in the database
            cursor.execute(f'''INSERT INTO {vehicle_id} (fuel_level, speed_level, temperature, fuel_alerts)
                               VALUES (?, ?, ?, ?)''', (vehicle_data['fuel_level'], vehicle_data['speed_level'],
                                                        vehicle_data['temperature'], vehicle_data['fuel_alerts']))
            conn.commit()

            # Print the generated data
            print(f"Vehicle: {vehicle_id}, Data: {vehicle_data}")

        await asyncio.sleep(2)  # Generate data every 2 seconds

# Start the data generation process
asyncio.run(generate_data())
