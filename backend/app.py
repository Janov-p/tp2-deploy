import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables from .env file
load_dotenv()

# Create the Flask application instance
app = create_app()

if __name__ == '__main__':
    # Development settings
    app.run(debug=True)
