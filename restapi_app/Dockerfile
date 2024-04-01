# Use the official Python image as a base image
FROM python:3.10-slim


# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project code into the container
COPY . /app/

# Expose port 8000 to allow communication to/from the Docker container
EXPOSE 8000

# Command to run the 

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
