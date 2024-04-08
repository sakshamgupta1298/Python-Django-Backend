# Docker Compose Setup for Temperature Monitoring System

This Docker-compose configuration sets up a system for monitoring temperature readings. It consists of three services:


1. **django_app**: A Django application that provides REST APIs for managing temperature readings for different cities and upload temperature data files. It also uses JWT token for Authorization.
2. **database**: A PostgreSQL database to store temperature readings.
3. **redis**: Message broker for Celery for task queueing.

Detailed explaination is covered for the above services in their respective README files in the directories: ./restapi_app

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


### django_app

This service hosts a Django application designed to monitor temperature readings for various cities. Access to the application is provided through port 8000. Currently, superuser credentials can be utilized for both authentication and authorization purposes.

One of the key features of this application is the "Upload Temperature File" functionality. This feature enables users to upload temperature data files, Upon receiving a file, the application uploads it to MinIO and passes the file's URL as an argument to a Celery task ,which are then processed asynchronously using Celery tasks. The processed data is subsequently , During file processing , the file is downloaded into a temporary folder, its data is read in chunks, and each chunk is processed to stored in the database.

For further details and instructions, please consult the README File located in the ./restapi_app directory.

Additionally, a Per-Site Cache Strategy has been implemented. This strategy is employed because the temperature statistics returned by the application endpoint are not specific to individual users.



### database

This service provides a PostgreSQL database to store temperature readings. It uses the latest PostgreSQL image and initializes the database with the provided environment variables.
This supports both Tables: `cache_table`, `temperature`.

## Configuration

You can modify the configuration of the services by editing the `docker-compose.yml` file. For example, you can adjust environment variables, port mappings, or volume mounts according to your requirements.

## Stopping the Services

To stop the services and remove the containers, networks, and volumes created by Docker-compose, press `Ctrl + C` in the terminal where Docker-compose is running, and then run:

```bash
docker-compose down 
```
## Authors
- Saksham Gupta
