from flask import Flask
from flask_cors import CORS
from src.landing.api import landing_api
from src.inventory.api import inventory_api
import os

app = Flask(__name__)
app.secret_key = os.environ.get('APP_SECRET')
app.register_blueprint(landing_api)
app.register_blueprint(inventory_api)
cors = CORS(app, resources={r"/vHub/*": {"origins": "*"}})

app.secret_key = os.environ.get('APP_SECRET')
