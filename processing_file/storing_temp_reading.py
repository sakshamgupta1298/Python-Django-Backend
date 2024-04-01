import psycopg2

# Define a class to represent the composite key (city_id, timestamp) along with temperature
class TemperatureReading:
    def __init__(self, city_id, timestamp, temperature):
        self.city_id = city_id
        self.timestamp = timestamp
        self.temperature = temperature

# Function to create the temperature readings table with primary key
def create_table():
    conn = psycopg2.connect(
        dbname="temperatures_db",
        user="postgres",
        password="123456789",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    # Create table if not exists with primary key on timestamp column
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS temperatures_db.public.temperature (
            city_id INT NOT NULL,
            temperature INT NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            UNIQUE (city_id, timestamp)  
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

# Function to insert temperature reading into the table
def insert_reading(reading):
    conn = psycopg2.connect(
        dbname="temperatures_db",
        user="postgres",
        password="123456789",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    # Insert data into the table
    cursor.execute("""
        INSERT INTO temperatures_db.public.temperature (city_id, temperature, timestamp)
        VALUES (%s, %s, %s)
    """, (reading.city_id, reading.temperature, reading.timestamp))

    conn.commit()
    cursor.close()
    conn.close()

# Sample usage
if __name__ == "__main__":
    # Create the table
    create_table()

    # Create sample TemperatureReading objects
    reading1 = TemperatureReading(144567, "2024-03-29 12:00:01", 33)
    reading2 = TemperatureReading(234566, "2024-03-29 12:15:01", 35)
    reading3 = TemperatureReading(1234567, "2024-03-29 12:30:01", 27)

    # Insert sample data
    insert_reading(reading1)
    insert_reading(reading2)
    insert_reading(reading3)
