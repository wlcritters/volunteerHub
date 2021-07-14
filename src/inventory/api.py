from flask import Blueprint

inventory_api = Blueprint('inventory_api', __name__, template_folder="templates", static_folder='static',
                          static_url_path="/static/inventory/")
