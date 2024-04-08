from tempfile import NamedTemporaryFile
from celery import shared_task
from temperature_api.models import TemperatureReading
import os
import time
import requests

@shared_task
def save_to_database(file_url):
    try:
        # Download the file content from the URL
        response = requests.get(file_url)
        response.raise_for_status()  # Raise an error if the request fails

        file_data = response.text  # Get the file content

        # Process the file data
        process_file_data(file_data)

    except Exception as e:
        # Handle exceptions
        print(f"Error occurred: {e}")
        raise RuntimeError("Unable to process file data.")

def process_file_data(file_data):
    # Create a temporary file to store the data
    with NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(file_data.encode())

        # Flush the data to ensure it's written to disk
        temp_file.flush()

        # Get the path of the temporary file
        temp_file_path = temp_file.name

        # Read the file data in chunks and process them
        with open(temp_file_path, 'r') as f:
            chunk_size = 1000 # Adjust as needed
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                process_chunk(chunk)

    f.close()
    # Delete the temporary file
    os.unlink(temp_file_path)

def process_chunk(chunk):
    max_retries = 3
    retry_delay = 5
    lines = chunk.split('\n')
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
