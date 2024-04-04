# Temperature Project

The Temperature Project is a Django-based web application designed to manage temperature readings for various cities. It allows authenticated users to view temperature statistics for a specific city and upload temperature data files.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Make sure you have the following software installed on your machine:

- Docker
- Python 3.10
- Celery and Redis

### Installing

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/sakshamgupta1298/Python-Django-Backend.git
    cd restapi_app
    ```

2. Build the Docker image:

    ```bash
    docker build -t django-temp-app .
    ```

3. Run the Docker container:

    ```bash
    docker run -p 8000:8000 django-temp-app
    ```

4. Access the application in your web browser at [http://localhost:8000](http://localhost:8000).

## Usage

### Creating Superuser

To create a superuser in a Django project, you can use the following command:

```bash
docker exec -it <container_id> python manage.py createsuperuser
```
Replace <container_id> with the ID or name of your Docker container running the Django project. This command will prompt you to enter a username, email address, and password for the superuser.


### Authentication

To access protected endpoints, you need to authenticate using JWT (JSON Web Tokens). Follow these steps to obtain a JWT access token:

1. Use the following endpoint to request a JWT token by providing your username and password(use the one that you created above) in the request body:

    ```
    POST /api/token/
    ```

    Example request body:
    ```json
    {
        "username": "your_username",
        "password": "your_password"
    }
    ```

    Example response:
    ```json
    {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
    ```

2. Copy the `access` token from the response.



### Endpoints

- `/temperature-readings/<int:city_id>/`: Retrieves temperature statistics (mean, max, min) for a specific city.
Methods: POST

To access protected endpoints, include the JWT access token in the request headers .
When using Postman, navigate to the Authorization section and choose "Bearer Token" as the authentication type. Paste your access token into the provided Token input box. Afterward, send the request.

-`/upload/`:  Allows users to upload temperature data files.
Methods: GET, POST

#### Caching of the GET REST Endpoint
For caching, I have used the in-built Django caching backemd that caches the result of the GET REST Endpoint in PostgresSQL database `cache_table`. Caching Strategy used is: Per-Site Cache Strategy because the temperature statistics returned by above endpoint is not user-specific.
API Response Performance improvement: 151 ms to 76 ms.

#### Celery for processing the Uploaded file
I have used celery which is responsible for managing background tasks, including the processing of uploaded temperature data files. This separation of tasks from the main web server process enhances scalability and performance. Additionally, used Redis serves as the message broker for Celery, facilitating communication between the Django application and Celery workers through a rapid and effective message queuing system.

## Built With

- Django - The web framework used
- PostgreSQL - Database for storing temperature readings
- Docker - Containerization for portability and easy deployment
- Celery - Distributed task queue for asynchronous processing

## Authors
- Saksham Gupta


