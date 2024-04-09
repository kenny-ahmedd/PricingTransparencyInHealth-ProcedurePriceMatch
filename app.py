# app.py in the root folder:
import os
import logging
from flask import Flask
from sqlalchemy import text

from extensions import db, redis_client
from views.comprehend_medical_service import comprehend_medical_blueprint
from views.hospital_charges_view import hospital_charges_view
from views.city_view import city_view
from views.hospital_view import hospital_view
from views.payer_view import payer_view
from views.zipcode_view import zipcode_view
from dotenv import load_dotenv

from flask_cors import CORS

from flask_redis import FlaskRedis

# Initialize logging
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
db.init_app(app)

# After initializing your app
app.config['REDIS_URL'] = "redis://localhost:6379/0"
redis_client.init_app(app)

app.register_blueprint(hospital_charges_view)

# Register the Blueprint
app.register_blueprint(comprehend_medical_blueprint)

# Register the city_view Blueprint
app.register_blueprint(city_view)

# Register the hospital_view Blueprint
app.register_blueprint(hospital_view)

# Register the payer_view Blueprint
app.register_blueprint(payer_view)

# Register the zipcode_view Blueprint
app.register_blueprint(zipcode_view)


# Function to test database connection
def test_db_connection():
    try:
        with app.app_context():
            with db.engine.connect() as connection:
                # Using the text() construct to execute a simple query
                result = connection.execute(text("SELECT 1"))
                for row in result:
                    logging.info("Database connection test was successful. Result: {}".format(row))
    except Exception as e:
        logging.error(f"Database connection test failed: {e}")


if __name__ == '__main__':
    with app.app_context():
        test_db_connection()
        db.create_all()
    app.run(debug=True)