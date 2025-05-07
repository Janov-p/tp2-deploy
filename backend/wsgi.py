import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables from .env file
load_dotenv()

# Create the Flask application instance with production config
app = create_app('production')

# Set production-specific configurations
app.config['FLASK_ENV'] = 'production'
app.config['DEBUG'] = False

if __name__ == '__main__':
    # Production settings - Cloud Run will set PORT automatically
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
