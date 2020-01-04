from functools import wraps
from flask import session
from .responses import error_response


def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if 'user' not in session:
      return error_response('Unauthorized', 401)
    return f(*args, **kwargs)
  return decorated
