# Docker Compose Setup for Temperature Monitoring System

This Docker-compose configuration sets up a system for monitoring temperature readings. It consists of three services:

1. **save_and_store_service**: A Python script to read temperature readings from a file and store them in a PostgreSQL database.
2. **django_app**: A Django application that provides REST APIs for monitoring temperature readings for different cities. It also uses JWT token for Authorization.
3. **database**: A PostgreSQL database to store temperature readings.

Detailed explaination is covered for the above services in their respective README files in the directories: ./processing_file and ./restapi_app

## Prerequisites

Ensure that you have Docker and Docker-compose installed on your machine.

## Usage

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/sakshamgupta1298/Python-Django-Backend.git
    ```

2. Navigate to the directory that you have cloned - that have docker-compose.yml.

3. Run the following command to start the services:

    ```bash
    docker-compose up --build
    ```

    This command will build the Docker images (if they don't exist) and start the containers for all services defined in the Docker-compose file.

4. Once the containers are up and running, you can access the Django application at [http://localhost:8000](http://localhost:8000).

## Services

### save_and_store_service

This service runs a Python script to read temperature readings from a file and store them in the PostgreSQL database.
For more details, refer the README File in ./processing_file directory.

### django_app

This service hosts a Django application for monitoring temperature readings for different cities. It exposes port 8000 to access the application. (For now, you can use your superuser credentials for Authentication and then Authorization.)
For more details, refer the README File in ./restapi_app directory.

### database

This service provides a PostgreSQL database to store temperature readings. It uses the latest PostgreSQL image and initializes the database with the provided environment variables.

## Configuration

You can modify the configuration of the services by editing the `docker-compose.yml` file. For example, you can adjust environment variables, port mappings, or volume mounts according to your requirements.

## Stopping the Services

To stop the services and remove the containers, networks, and volumes created by Docker-compose, press `Ctrl + C` in the terminal where Docker-compose is running, and then run:

```bash
docker-compose down 
```
## Authors
- Saksham Gupta
