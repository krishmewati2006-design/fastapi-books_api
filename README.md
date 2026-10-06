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

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://127.0.0.1:8000/docs`
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

