import random
from datetime import datetime,timedelta

# Function to generate random timestamp
def random_timestamp():
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2022, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    random_time = random.random() * 86400  # seconds in a day
    return start_date + timedelta(days=random_days, seconds=random_time)

# Generate sample data and write to file
with open("sample_data.txt", "w") as file:
    for _ in range(1000):
        city_id = random.randint(1, 100)
        temperature = random.randint(-20, 40)  # Assuming temperature in Celsius
        timestamp = random_timestamp().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{city_id},{temperature},{timestamp}\n")
