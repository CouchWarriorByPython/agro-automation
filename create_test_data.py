import requests
import random
from datetime import datetime, timedelta

# Configuration
base_url = "http://localhost:8000"
plants = [
    "Tomato", "Cucumber", "Lettuce", "Carrot", "Pepper",
    "Eggplant", "Broccoli", "Spinach", "Potato", "Radish"
]
num_days = 5
measurements_per_day = 20

# Function to generate random float numbers within a range
def random_float(minimum, maximum, decimals=2):
    number = random.uniform(minimum, maximum)
    return float(f"{number:.{decimals}f}")


# Create plants with reference data
for plant in plants:
    plant_data = {
        "plant_name": plant.lower(),  # Ensure plant name is in lowercase
        "reference_humidity": random_float(40, 70),  # Random reference humidity
        "reference_minerals": random_float(10, 50),  # Random mineral percentage
        "reference_temperature": random_float(10, 30)  # Random temperature value
    }
    response = requests.post(f"{base_url}/add-plant", json=plant_data)
    if response.status_code == 200:
        print(f"Plant '{plant}' added successfully.")
    else:
        print(f"Error adding plant '{plant}': {response.text}")

# Create daily measurements for each plant for the past 5 days
start_date = datetime.now().date() - timedelta(days=num_days)
for day in range(num_days):
    measurement_date = start_date + timedelta(days=day)
    for plant in plants:
        for _ in range(measurements_per_day):
            measurement_data = {
                "plant_name": plant.lower(),  # Using lowercase plant name
                "date": measurement_date.isoformat(),
                "soil_moisture_content": random_float(30, 80),  # Random moisture content
                "amount_of_mineral_substance": random_float(10, 100),  # Random mineral substance amount
                "temperature_conditions": random_float(15, 35)  # Random temperature
            }
            response = requests.post(f"{base_url}/daily-plant-data", json=measurement_data)
            if response.status_code == 200:
                print(f"Measurement for '{plant}' on {measurement_date} added successfully.")
            else:
                print(f"Error adding measurement for '{plant}' on {measurement_date}: {response.text}")

print("Data generation complete.")
