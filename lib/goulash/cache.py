""" goulash.cache

    dumb lightweight caching decorator.  this requires werkzeug,
    but at least avoids a memcache dependency.
"""
import time

from functools import wraps

from werkzeug.contrib.cache import SimpleCache

cache = SimpleCache()

def cached(cache_key, timeout=5 * 60):
    """ adapted from http://flask.pocoo.org/docs/patterns/viewdecorators/ """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            rv = cache.get(cache_key)
            if rv is not None:
                return rv
            rv = f(*args, **kwargs)
            cache.set(cache_key, rv, timeout=timeout)
            return rv
        return decorated_function
    return decorator
