import multiprocessing
import psycopg2
from psycopg2 import sql
import argparse

# Function to process the file and put data into the queue
def process_file_and_queue(file_path, queue,num_processes):
    with open(file_path, 'r') as file:
        for line in file:
            queue.put(line.strip())
    # Signal termination to the queue
    print(queue)
    for _ in range(num_processes):
        queue.put(None)

# Function to save data to the database
def save_to_database(queue):
    conn = psycopg2.connect(
        dbname="temperatures_db",
        user="postgres",
        password="123456789",
        host="host.docker.internal",  # Use this special DNS name to refer to the host machine
        port="5432"
    )
    cursor = conn.cursor()
    print("Connected to db")

    while True:
        data = queue.get()
        if data is None:
            # If the sentinel value is received, break out of the loop
            break
        city_id, temperature, timestamp = data.split(',')
        query = sql.SQL("INSERT INTO temperatures_db.public.temperature (city_id, temperature, timestamp) VALUES (%s, %s, %s)")
        cursor.execute(query, (city_id, temperature, timestamp))
    
    conn.commit()
    cursor.close()
    conn.close()


# Main function
def main():
    parser = argparse.ArgumentParser(description='Process a file and save data to the database.')
    parser.add_argument('file', type=str, help='Path to the input file')
    args = parser.parse_args()

    file_path = args.file

    
    # Initialize queue
    manager = multiprocessing.Manager()
    queue = manager.Queue()

    # Define the number of processes
    num_processes = multiprocessing.cpu_count()

    # Start a single process to read the file and put data into the queue
    file_process = multiprocessing.Process(target=process_file_and_queue, args=(file_path, queue,num_processes))
    file_process.start()

    # Start a single process to save data to the database
    print(queue)
    save_to_database(queue)

    # Wait for the file processing process to finish
    file_process.join()

if __name__ == "__main__":
    main()
