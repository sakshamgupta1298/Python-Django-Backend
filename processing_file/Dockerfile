# Use an official Python runtime as the base image
FROM python:3.10-slim


# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the script and data file into the container
COPY save_and_store_reading.py /app/
COPY sample_data.txt /app/

# Install Python dependencies
RUN pip install psycopg2-binary

# Command to run the Python script
CMD ["python", "save_and_store_reading.py"]
