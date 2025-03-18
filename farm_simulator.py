
import requests
import random
import time
from datetime import datetime
import os

# Configuration
API_KEY = os.environ.get("IOT_API_KEY")
BASE_URL = "http://0.0.0.0:5000"

def simulate_resource_usage(resource_id, resource_type):
    """Simulate resource usage over time"""
    while True:
        # Get current resource amount
        headers = {"X-API-Key": API_KEY}
        try:
            response = requests.get(
                f"{BASE_URL}/api/farm-resources",
                headers=headers
            )
            resources = response.json()['resources']
            resource = next((r for r in resources if r['id'] == resource_id), None)
            
            if not resource:
                print(f"Resource {resource_id} not found")
                return
                
            # Simulate usage based on resource type
            if resource_type == "water":
                usage = random.uniform(0.5, 2.0)  # Liters per minute
            elif resource_type == "fertilizer":
                usage = random.uniform(0.1, 0.5)  # kg per hour
            else:
                usage = random.uniform(0.1, 0.3)  # Generic usage
                
            new_amount = max(0, resource['amount'] - usage)
            
            # Update resource amount
            response = requests.put(
                f"{BASE_URL}/api/farm-resources/{resource_id}",
                json={'amount': new_amount},
                headers=headers
            )
            print(f"Updated {resource_type}: {new_amount:.2f} {resource['unit']}")
            
        except Exception as e:
            print(f"Error updating resource: {e}")
            
        # Wait before next update
        time.sleep(60)  # Update every minute

if __name__ == "__main__":
    # Example usage - replace with actual resource ID
    RESOURCE_ID = 1  # The ID of your resource
    RESOURCE_TYPE = "water"  # The type of resource
    simulate_resource_usage(RESOURCE_ID, RESOURCE_TYPE)
