from src.authentication.auth import get_permissions, requires_auth
from flask_cors import CORS, cross_origin
from flask import Flask, jsonify, redirect, render_template, session, request
from six.moves.urllib.parse import urlencode
import os

app = Flask(__name__)

app.secret_key = os.environ.get('APP_SECRET')
WEB_HOST = os.environ.get('WEB_HOST')
CLIENT_ID = os.environ.get('CLIENT_ID')
AUTH0_URL = os.environ.get('AUTH0_URL')

cors = CORS(app, resources={r"/vHub/*": {"origins": "*"}})


@app.route('/vHub', methods=['GET'])
@app.route('/vHub/', methods=['GET'])
@cross_origin(headers=["Content-Type", "Authorization"])
def main_menu():
    return render_template('index.html')


@app.route('/vHub/apps', methods=['GET'])
@cross_origin(headers=["Content-Type", "Authorization"])
def get_available_apps():
    permissions = get_permissions()
    return jsonify({'success': True,
                    'permissions': permissions})


@app.route("/vHub/tokenAuth", methods=['GET'])
def token_auth():
    session['token'] = request.args.get('token')
    return redirect('/vHub/')


@app.route('/vHub/logout', methods=['GET'])
def logout():
    session.clear()
    params = {'returnTo': WEB_HOST, 'client_id': CLIENT_ID}
    return redirect("https://" + AUTH0_URL + '/v2/logout?' + urlencode(params))
