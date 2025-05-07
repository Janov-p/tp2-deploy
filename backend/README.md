# Flask Authentication API

A secure RESTful API built with Flask, featuring JWT authentication, database migrations, and API documentation.

## Features

- JWT-based authentication
- User registration and login
- Token refresh mechanism
- Secure password hashing
- Database migrations with Alembic
- API documentation with Swagger/OpenAPI
- Environment-based configuration
- SQLAlchemy ORM

## Project Structure

```
backend/
├── app/
│   ├── __init__.py          # Application factory
│   ├── auth/                # Authentication module
│   │   ├── __init__.py
│   │   ├── api.py          # API endpoints and documentation
│   │   ├── models.py       # User model
│   │   ├── routes.py       # Route handlers
│   │   └── utils.py        # Utility functions
│   └── main/               # Main application module
│       ├── __init__.py
│       └── routes.py       # Main routes
├── instance/               # Instance-specific files (not in version control)
│   ├── .gitkeep           # Keeps the folder in version control
│   └── app.db             # SQLite database (created automatically)
├── migrations/             # Database migrations
├── .env.example           # Example environment variables
├── alembic.ini            # Alembic configuration
├── app.py                 # Application entry point
├── config.py              # Configuration settings
└── requirements.txt       # Project dependencies
```

## Setup

1. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create environment file:
```bash
cp .env.example .env
```

4. Update the `.env` file with your configuration:
```
FLASK_ENV=development
JWT_SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///instance/app.db
```

5. Create instance folder (if not exists):
```bash
mkdir -p instance
```

6. Initialize the database:
```bash
alembic upgrade head
```

## Running the Application

Development mode:
```bash
python app.py
```

Production mode:
```bash
export FLASK_ENV=production
python app.py
```

## API Documentation

Once the application is running, visit:
```
http://localhost:5000/
```

## API Endpoints

### Authentication

- `POST /auth/register` - Register new user
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword",
    "name": "User Name"
  }
  ```

- `POST /auth/login` - Login
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword"
  }
  ```

- `POST /auth/refresh` - Refresh access token
  - Requires refresh token in Authorization header

- `POST /auth/logout` - Logout
  - Requires access token in Authorization header

- `GET /auth/me` - Get current user info
  - Requires access token in Authorization header

### Main

- `GET /` - Home endpoint

## Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback one migration:
```bash
alembic downgrade -1
```

## Security Features

- JWT token-based authentication
- Password hashing with Werkzeug
- Token blacklisting for logout
- Environment-based configuration
- Secure cookie settings in production
- CSRF protection

## Development

1. Make changes to models in `app/auth/models.py`
2. Create and apply migrations:
```bash
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

3. Update API documentation in `app/auth/api.py`

## Instance Folder

The `instance` folder is a special directory in Flask applications that contains instance-specific files. This folder is not tracked in version control (except for the `.gitkeep` file) and is used for:

- Database files (e.g., SQLite database)
- Configuration files with sensitive information
- Instance-specific data
- Temporary files

The instance folder is automatically created by Flask when needed, but you can also create it manually. Files in this folder are not committed to version control to keep sensitive information secure.

To use the instance folder in your code:
```python
from flask import current_app

# Access instance folder path
instance_path = current_app.instance_path

# Access a file in the instance folder
file_path = os.path.join(current_app.instance_path, 'filename.txt')
```

## Production Deployment

1. Set environment variables:
```