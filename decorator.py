from functools import wraps
from flask import request, Response
from werkzeug.security import generate_password_hash, check_password_hash

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and check_password_hash('pbkdf2:sha256:50000$D26bTDeg$2029ec6b9290c90be0103db91df21e22a387095a20d43792e4920d6c00b98db3',password)
#How to make password hash
#python
#>>> from werkzeug.security import generate_password_hash
#>>> generate_password_hash("your_password")

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated