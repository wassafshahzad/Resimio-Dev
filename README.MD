# Django Booking Management Application

This is a Django-based booking management system for facilities, featuring user management and booking functionality. It includes features for managing bookings, listing available facilities, and handling user authentication.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Setup](#setup)
- [Running the Application](#running-the-application)
- [Admin and Regular User Credentials](#admin-and-regular-user-credentials)
- [Testing](#testing)
- [Docker Setup](#docker-setup)
- [Running Tests in Docker](#running-tests-in-docker)

## Prerequisites

Before setting up the application, ensure that you have the following installed:

- docker
- docker-compose

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://your-repository-url.git
    cd your-repository-folder
    ```

2. **Running Docker container:**

    ```bash
    docker-compose build
    docker-compose up
    ```

## Setup

1. **Configure the environment variables**:

    The .env file is available in the repo itself, this is not a good practice and is only for testing purposes 

2. **Set up the database**:

    The database is already setup and 2 initial users are also provided so you don't have to create your own.

    - **Superuser**:
        - Email: `admin@example.com`
        - Username: `admin`
        - Password: `adminpassword`

    - **Regular user**:
        - Email: `user@example.com`
        - Username: `regularuser`
        - Password: `userpassword`

## Running the Application

1. **Run the development server:**
    This should start the server and database.
    ```bash
    docker-compose build
    docker-compose up
    ```

    The application will be accessible at `http://127.0.0.1:8000/`.

2. **Access the Django Admin panel**:

    Go to `http://127.0.0.1:8000/admin/` and log in using the superuser credentials:

    - **Email**: `admin@example.com`
    - **Password**: `adminpassword`

3. **User authentication**:

    - **Login as regular user**:
        - **Email**: `user@example.com`
        - **Password**: `userpassword`

    After logging in, the user can view and manage their bookings.

## Testing

To run the tests, use the following command, Make suer the container is runnning

```bash
docker-compose exec python manage.py test
