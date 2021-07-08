import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'udacity-fsnd.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'dev'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

# Unpack the request header
def get_token_auth_header():
    # raise an AuthError if no header is present
    if 'Authorization' not in request.headers:
        abort(401)

    auth_header = request.headers['Authorization']
    # split bearer and the token
    header_parts = auth_header.split(' ')

    # raise an AuthError if the header is malformed
    if len(header_parts) != 2:
        abort(401)
    elif header_parts[0].lower() != 'bearer':
        abort(401)

    # return the token part of the header
    return header_parts[1]

# Verify that authorization header includes permissions
def check_permissions(permission, payload):
    # permissions are not included in the payload
    if 'permissions' not in payload:
        abort(403)
    # requested permission string is not in the payload permissions array
    if permission not in payload['permission']:
        abort(403)
    # otherwise return True to indicate that that permission exists without problems
    return True

# Verify that a JWT is authentic and decode it
def verify_decode_jwt(token):
    # get the public key from auth0
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    # get the data in the header
    unverified_header = jwt.get_unverified_header(token)

    # choose our key
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

    # finally, verify
    if rsa_key:
        try:
            # decode the payload from the token
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            # return the decoded payload
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

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(token)
            except:
                abort(401)
            # make sure permission exists in JWT
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator