""" goulash.decorators
"""
import inspect
import sys

#based on http://code.activestate.com/recipes/578852-decorator-to-check-if-needed-modules-for-method-ar/
def require_module(names, exception=None):
    """
    Check if needed modules imported before run method

    Example::

        @require_module(['time'],exception=Exception)
        def get_time():
            return time.time()
    """
    if isinstance(names, (str, unicode)):
        names=[names]
    def check_module(f):
        def new_f(*args, **kwds):
            for module_name in names:
                if module_name not in sys.modules.keys():
                    if exception:
                        err = ('Module "{0}" is required for {1}.  '
                               'Try running `pip install {2}` first.')
                        err = err.format(
                            module_name, f.func_name, module_name)
                        raise exception(err)
                    else:
                        return None
            return f(*args, **kwds)
        new_f.func_name = f.func_name
        return new_f
    return check_module


class arg_types(object):
    """ A decorator which enforces the rule that all arguments must be
        of type .  All keyword arguments are ignored. Throws ArgTypeError
        when expectations are violated.

        Example usage follows:

          @arg_types(int, float)
          def sum(*args): pass
    """

    class ArgTypeError(TypeError): pass

    def __init__(self, *args):
        err = 'all arguments to arg_types() should be types, got {0}'
        assert all([inspect.isclass(a) for a in args]), err.format(args)
        self.types = args

    def __call__(self, fxn):
        self.fxn = fxn
        def wrapped(*args, **kargs):
            for a in args:
                if not isinstance(a, self.types):
                    raise self.ArgTypeError("{0} (type={1}) is not in {2}".format(
                        a, type(a), self.types))
            return self.fxn(*args, **kargs)
        return wrapped

class memoized_property(object):
    """
    A read-only @property that is only evaluated once.

    From: http://www.reddit.com/r/Python/comments/ejp25/cached_property_decorator_that_is_memory_friendly/
    """
    def __init__(self, fget, doc=None):
        self.fget = fget
        self.__doc__ = doc or fget.__doc__
        self.__name__ = fget.__name__

    def __get__(self, obj, cls):
        if obj is None:
            return self
        obj.__dict__[self.__name__] = result = self.fget(obj)
        return result
