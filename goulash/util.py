""" goulash.util
"""
import time, uuid
from goulash._os import home

def summarize_fpath(fpath):
    """ truncates a filepath to be more suitable for display.
        every instance of $HOME is replaced with ~
    """
    if home():
        return fpath.replace(home(), '~')

def uniq(use_time=False):
    """ """
    result = str(uuid.uuid1())
    if use_time:
        result += str(time.time())[:-3]
    return result
