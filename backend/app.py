import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables from .env file
load_dotenv()

app = create_app()

if __name__ == '__main__':
    env = app.config['FLASK_ENV']
    
    if env == 'production':
        # Production settings - Cloud Run will set PORT automatically
        port = int(os.getenv('PORT', 8080))
        app.run(host='0.0.0.0', port=port, debug=False)
    else:
        # Development settings
        app.run(debug=True)
