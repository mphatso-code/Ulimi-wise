
import requests
import random
import time
from datetime import datetime

# Configuration
API_KEY = os.environ.get("IOT_API_KEY")  # Get API key from environment
BASE_URL = "http://0.0.0.0:5000"

def simulate_sensor(sensor_id, sensor_type):
    """Simulate sensor readings"""
    while True:
        # Generate mock sensor data
        if sensor_type == "soil_moisture":
            value = random.uniform(0, 100)  # Percentage
        elif sensor_type == "temperature":
            value = random.uniform(15, 35)  # Celsius
        elif sensor_type == "humidity":
            value = random.uniform(30, 90)  # Percentage
        
        # Generate mock device stats
        battery_level = random.uniform(50, 100)
        signal_strength = random.uniform(70, 100)
        
        # Prepare the reading data
        data = {
            "sensor_id": sensor_id,
            "value": value,
            "battery_level": battery_level,
            "signal_strength": signal_strength
        }
        
        # Send the reading
        headers = {"X-API-Key": API_KEY}
        try:
            response = requests.post(
                f"{BASE_URL}/api/sensors/{sensor_id}/readings",
                json=data,
                headers=headers
            )
            print(f"Sent reading: {data}")
            if response.status_code != 200:
                print(f"Error: {response.json()}")
        except Exception as e:
            print(f"Error sending reading: {e}")
            
        # Wait before next reading
        time.sleep(60)  # Send reading every minute

if __name__ == "__main__":
    # Example usage - replace with your actual sensor ID
    SENSOR_ID = 1  # The ID of your sensor from the database
    SENSOR_TYPE = "soil_moisture"  # The type of your sensor
    simulate_sensor(SENSOR_ID, SENSOR_TYPE)
