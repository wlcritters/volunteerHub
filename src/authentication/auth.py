import json
import os
from flask import request, session
from functools import wraps
from jose import jwt, JWTError
from urllib.request import urlopen


AUTH0_DOMAIN = os.environ.get('AUTH0_URL')
ALGORITHMS = os.environ.get('ALGORITHMS')
API_AUDIENCE = os.environ.get('AUD')

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header


def get_token_auth_header():
    auth_header = request.headers.get("Authorization", None)
    return validate_auth_header(auth_header)

def get_token_session():
    response = ""
    if 'token' in session:
        response = session['token']
    return response


def validate_auth_header(auth_header):
    if auth_header is not None:
        split = auth_header.split()
        if len(split) == 2 and split[0].upper() == "BEARER":
            return split[1]
    raise AuthError({"code": "Invalid_Token_Auth",
                     "description": "Authorization token is expected"}, 401)


def check_permissions(permission, payload):
    if payload.get('permissions') is not None and permission in payload.get('permissions'):
        return True
    raise AuthError({"code": "Invalid_Permissions",
                     "description": "Valid Permissions Expected"}, 401)


def verify_decode_jwt(token):
    url = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(url.read())
    try:
        unverified_header = jwt.get_unverified_header(token)
    except JWTError:
        raise AuthError({
            'code': 'invalid_token',
            'description': 'token is invalid'
        }, 400)

    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    if rsa_key:
        try:
            # USE THE KEY TO VALIDATE THE JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key.'
    }, 400)


def get_permissions():
    try:
        token = get_token_session()
        payload = verify_decode_jwt(token)
        response = payload.get('permissions')
        print(response)
        if response is None or response.size == 0:
            response = ['logout']
    except AuthError:
        response = []
    return response


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator