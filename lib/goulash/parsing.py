""" goulash.parsing
"""

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    # utility to strip html which only requires the pyton stdlib.  taken from:
    #  http://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
