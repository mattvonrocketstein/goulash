""" goulash.wrappers """

class JSONWrapper(object):
    """ convenience wrapper """
    def __init__(self, data):
        self._data = data
    def __getattr__(self, name):
        try:
            return self._data[name]
        except KeyError:
            return getattr(self._data, name)
    __getitem__ = __getattr__
