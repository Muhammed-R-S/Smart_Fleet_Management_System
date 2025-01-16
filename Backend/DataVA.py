import asyncio
import websockets
import json
import sqlite3
from datetime import datetime

# Create a SQLite3 database connection
conn = sqlite3.connect('vehicle_data.db')
cursor = conn.cursor()

async def send_latest_data(websocket, path):
    try:
        while True:
            # Fetch the latest data from VehicleA table in the database
            cursor.execute("SELECT * FROM VehicleA ORDER BY timestamp DESC LIMIT 1")
            latest_data = cursor.fetchone()

            if latest_data:
                vehicle_data = {
                    'fuel_level': latest_data[2],  # Index 2 corresponds to fuel_level in the fetched data
                    'speed_level': latest_data[3],  # Index 3 corresponds to speed_level
                    'temperature': latest_data[4],  # Index 4 corresponds to temperature
                    'fuel_alerts': latest_data[5]  # Index 5 corresponds to fuel_alerts
                }

                # Send the latest data to the client
                await websocket.send(json.dumps({'latest_vehicle_data': vehicle_data}))

            await asyncio.sleep(2)  # Send data every 2 seconds
    except websockets.exceptions.ConnectionClosedOK:
        print("Connection ...")

async def send_historical_data(websocket, path):
    # Example query to fetch data from a database table
    cursor.execute("SELECT * FROM VehicleA")
    data = cursor.fetchall()

    # Convert data to JSON format
    json_data = json.dumps(data)

    # Send the JSON data to the client
    await websocket.send(json_data)

           
# Start both WebSocket servers
start_server_latest_data = websockets.serve(send_latest_data, "localhost", 8000)
start_server_historical_data = websockets.serve(send_historical_data, "localhost", 8004)

asyncio.get_event_loop().run_until_complete(start_server_latest_data)
asyncio.get_event_loop().run_until_complete(start_server_historical_data)
asyncio.get_event_loop().run_forever()
