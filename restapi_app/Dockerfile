# Use an official Python runtime as a parent image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
# RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port 8000 to allow communication to/from server
EXPOSE 8000

# Install Redis server
RUN apt-get update && apt-get install -y redis-server

# Run Redis server
CMD redis-server & celery -A temperature_project worker --pool=solo -l info & python manage.py runserver 0.0.0.0:8000
