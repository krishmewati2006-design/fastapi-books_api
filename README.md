# Books API

The Books API is a robust, production-ready RESTful service built with FastAPI for managing a library of books. It features a secure authentication system using JSON Web Tokens (JWT) and utilizes SQLAlchemy for database interactions with PostgreSQL.

## Features

- User Authentication: Secure registration and login system providing JWT tokens.
- Protected Endpoints: All book-related CRUD operations require a valid JWT token.
- CRUD Operations: Create, Read, Update, and Delete books from the collection.
- Database Migrations: Managed by Alembic to ensure consistent schema updates.
- Data Validation: Built-in validation using Pydantic models for request and response data.
- Modern Stack: Built with FastAPI, SQLAlchemy 2.0, and PostgreSQL.

## Technologies Used

- FastAPI: A modern, fast (high-performance), web framework for building APIs.
- SQLAlchemy: The Python SQL Toolkit and Object Relational Mapper.
- PostgreSQL: An advanced, open-source relational database.
- Alembic: A lightweight database migration tool for use with SQLAlchemy.
- Pydantic: Data validation and settings management using Python type annotations.
- Python Jose: A JavaScript Object Signing and Encryption implementation in Python.
- Passlib: A password hashing library for Python.

## Prerequisites

Before setting up the project, ensure you have the following installed:
- Python 3.10 or higher
- PostgreSQL
- pip (Python package installer)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd books_api
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The application uses environment variables for configuration. Create a `.env` file in the root directory (one is already provided in the source for development, but should be updated for production):

```env
DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<database_name>
SECRET_KEY=<your-secret-key>
```

Replace the placeholders with your actual PostgreSQL credentials and a secure secret key for JWT signing.

## Database Migrations

This project uses Alembic to manage database schema changes. To apply existing migrations and create the necessary tables, run:

```bash
alembic upgrade head
```

If you make changes to the models in `models.py`, generate a new migration with:

```bash
alembic revision --autogenerate -m "description of changes"
alembic upgrade head
```

## Running the Application

To start the FastAPI server locally, use Uvicorn:

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## Deployment (Docker Compose on AWS EC2)

Follow these steps to deploy the application on an AWS EC2 instance using Docker Compose:

# 1. Prerequisites on AWS & EC2
- An active AWS account with an **EC2 instance** (Ubuntu 22.04 LTS or Amazon Linux 2023 recommended).
- Configure the EC2 **Security Group** to allow inbound traffic on:
  - **SSH (Port 22)**: For server access.
  - **HTTP (Port 80)** or **API (Port 8000)**: To access the API.

# 2. Prepare the Docker Configuration
Ensure your repository includes a `Dockerfile` and a `docker-compose.yml` file.

## Deployment (Docker Compose on AWS EC2)

This project runs as two containers managed by Docker Compose: the FastAPI app (`api`) and PostgreSQL (`db`). The database stores its data in a named Docker volume, so data survives container restarts and rebuilds. Postgres is not exposed to the internet; only the API is.

### 1. Prerequisites

- An AWS EC2 instance running **Ubuntu LTS** (a `t3.micro` is enough for a demo).
- A **security group** with these inbound rules:
  - **SSH (port 22)**, source: your own IP only.
  - **Custom TCP (port 8000)**, source: your own IP only (or the addresses that need access).
- The `.pem` key file for the instance.

### 2. Connect and install Docker

```bash
ssh -i /path/to/your-key.pem ubuntu@<EC2-PUBLIC-IP>

sudo apt update && sudo apt install -y docker.io docker-compose-v2
sudo usermod -aG docker $USER
```

Log out and reconnect over SSH so the group change takes effect (then `docker` works without `sudo`).

### 3. Get the code and configure secrets

```bash
git clone https://github.com/krishmewati2006-design/fastapi-books_api.git
cd fastapi-books_api
```

Generate two random values:

```bash
openssl rand -hex 32   # use as SECRET_KEY
openssl rand -hex 16   # use as POSTGRES_PASSWORD
```

Create a `.env` file (`nano .env`) with these four variables:

```env
POSTGRES_USER=books_user
POSTGRES_PASSWORD=<generated-password>
POSTGRES_DB=books_db
SECRET_KEY=<generated-secret-key>
```

`.env` is listed in `.gitignore`. Never commit it. `docker-compose.yml` builds the `DATABASE_URL` from these values automatically.

### 4. Build and start

```bash
docker compose up -d --build
docker compose ps
```

`db` should show as **healthy** and `api` as **running**. Both are set to `restart: unless-stopped`, so they come back after a server reboot.

### 5. Create the database tables

On a fresh database, run the migrations once:

```bash
docker compose exec api alembic upgrade head
```

### 6. Verify

Open `http://<EC2-PUBLIC-IP>:8000/docs` in your browser. Use the **Authorize** button to log in and try the `/books` endpoints.

To read the application logs:

```bash
docker compose logs -f api
```

Press `Ctrl+C` to stop following the logs.

### Notes

- If you stop and start the instance, its **public IP changes**. If you can't connect, check the new IP and make sure your security group rules match your current IP.
- Do **not** run `docker compose down -v`. The `-v` flag deletes the database volume and all your data.
- The API runs over plain HTTP. For real use, put it behind HTTPS (for example with a reverse proxy and a certificate).


## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://<EC2-PUBLIC-IP>:8000/docs`
- Redoc: `http://127.0.0.1:8000/redoc`

## API Endpoints

### Authentication
- POST `/register`: Register a new user with a username and password.
- POST `/login`: Authenticate and receive an access token.

### Books (Requires Authentication)
- GET `/books`: Retrieve a list of all books.
- GET `/books/{book_id}`: Retrieve details of a specific book by its ID.
- POST `/books`: Add a new book to the collection.
- PUT `/books/{book_id}`: Update an existing book's details.
- DELETE `/books/{book_id}`: Remove a book from the collection.

## Authentication Usage

To access protected endpoints, include the JWT token in the `Authorization` header of your requests:

```
Authorization: Bearer <your-access-token>
```

You can obtain the token by successfully calling the `/login` endpoint.

# Update in '/login' Endpoint

/login now expects form fields, not JSON. Anything else that calls it, like a frontend or a curl test, must send username and password as form data like this:

curl -X POST -d "username=NAME&password=PASS" http://localhost:8000/login

