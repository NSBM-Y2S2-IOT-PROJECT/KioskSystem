from flask import Flask
from flask_cors import CORS
from routes import routes
from infoWrap import Info

# Initialize Flask app and logger
app = Flask(__name__)
CORS(app)

logger = Info()

# Register the routes Blueprint
app.register_blueprint(routes)

if __name__ == '__main__':
    logger.info("Starting VISUM Server System Backend...")
    app.run(host='0.0.0.0', port=5000)
