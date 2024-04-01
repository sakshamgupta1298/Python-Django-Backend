# Save and Store Temperature Readings

This Python script is designed to read temperature readings from a file and store them in a PostgreSQL database.

## Getting Started

These instructions will guide you on how to set up and run the script.

### Prerequisites

Before running the script, make sure you have the following installed on your machine:

- Docker
- Python 3.10

### Installing

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/yourusername/save-and-store-temperature-readings.git
    cd save-and-store-temperature-readings
    ```

2. Build the Docker image:

    ```bash
    docker build -t save-and-store-readings .
    ```

### Usage

1. Ensure you have a file containing temperature readings in the following format:

    ```
    city_id,temperature,timestamp
    ```

    Example:
    ```
    1,25.5,2024-04-01T12:00:00
    2,22.3,2024-04-01T12:15:00
    ```

2. Run the Docker container and pass the filename as an argument:

    ```bash
    docker run save-and-store-readings your_data_file.txt
    ```

    Replace `your_data_file.txt` with the path to your input file containing temperature readings.

3. The script will read the file, process the data, and store it in the PostgreSQL database.

## Configuration

The script connects to a PostgreSQL database to store the temperature readings. You can configure the database connection by modifying the following environment variables in the Dockerfile:

- `DB_NAME`: Name of the PostgreSQL database
- `DB_USER`: Username for connecting to the database
- `DB_PASSWORD`: Password for connecting to the database
- `DB_HOST`: Hostname of the PostgreSQL server
- `DB_PORT`: Port number of the PostgreSQL server

Ensure that the PostgreSQL server is accessible from within the Docker container.

## Built With

- Python - The programming language used
- psycopg2 - PostgreSQL adapter for Python
- Docker - Containerization for portability

## Authors

- Saksham Gupta


