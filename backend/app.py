import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables from .env file
load_dotenv()

app = create_app()

if __name__ == '__main__':
    env = app.config['FLASK_ENV']
    
    if env == 'production':
        # Production settings
        app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=False)
    else:
        # Development settings
        app.run(debug=True)
