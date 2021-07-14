from src.authentication.auth import get_permissions
from flask_cors import cross_origin
from flask import jsonify, redirect, render_template, session, request, Blueprint,url_for
from six.moves.urllib.parse import urlencode
import os

landing_api = Blueprint('landing_api', __name__, template_folder="templates", static_folder='static', static_url_path="/static/landing/")


WEB_HOST = os.environ.get('WEB_HOST')
CLIENT_ID = os.environ.get('CLIENT_ID')
AUTH0_URL = os.environ.get('AUTH0_URL')




@landing_api.route('/vHub/', methods=['GET'])
@cross_origin(headers=["Content-Type", "Authorization"])
def main_menu():
    return render_template('landing/index.html')


@landing_api.route('/vHub/apps', methods=['GET'])
@cross_origin(headers=["Content-Type", "Authorization"])
def get_available_apps():
    permissions = get_permissions()
    return jsonify({'success': True,
                    'permissions': permissions})


@landing_api.route("/vHub/tokenAuth", methods=['GET'])
def token_auth():
    session['token'] = request.args.get('token')
    return redirect('/vHub/')


@landing_api.route('/vHub/logout', methods=['GET'])
def logout():
    session.clear()
    params = {'returnTo': WEB_HOST, 'client_id': CLIENT_ID}
    return redirect("https://" + AUTH0_URL + '/v2/logout?' + urlencode(params))
