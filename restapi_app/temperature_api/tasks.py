from celery import shared_task
from temperature_api.models import TemperatureReading
import time

@shared_task
def save_to_database(file_data):
    max_retries = 3
    retry_delay = 5
    try:
        lines = file_data.split('\n')
        print(lines)
        for line_number, line in enumerate(lines, start=1):
            attempt = 0  # Initialize attempt counter
            while attempt < max_retries:
                attempt += 1
                try:
                    data = line.strip()
                    if not data:
                        continue
                    # Split the line into city_id, temperature, and timestamp
                    city_id, temperature, timestamp = data.split(',')
                    # Create a new Temperature object and save it to the database
                    TemperatureReading.objects.create(city_id=city_id, temperature=temperature, timestamp=timestamp)
                    # If successful, break out of the retry loop
                    break
                except ValueError as e:
                    # Handle the case where the line doesn't contain three values
                    print(f"Error processing line {line_number}: {e}")
                    print(f"Line content: {line}")
                except Exception as e:
                    # Handle other exceptions
                    print(f"Error processing line {line_number}: {e}")
                    print(f"Line content: {line}")
                if attempt < max_retries:
                    print(f"Retrying line in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    raise RuntimeError("Max retries reached. Unable to process line.")
    except Exception as e:
        # Handle exceptions related to reading file_data or splitting lines
        print(f"Error occurred: {e}")
        raise RuntimeError("Unable to process file data.")
