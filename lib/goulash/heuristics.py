""" goulash.heuristics
"""

from goulash.wrappers import DumbWrapper

class Answer(DumbWrapper):
    def __str__(self):
        return "({0}: {1})".format(
            self.__class__.__name__,
            str(self.obj))

    def __nonzero__(self):
        return bool(self.obj)

    __repr__ = __str__

class ExplainedAnswer(Answer):
    def __str__(self):
        return "({0}: {1})".format(
            self.__class__.__name__,
            str(self.explanation))

class NotApplicable(DumbWrapper):
    def __nonzero__(self):
        return False
    def __str__(self):
        return "(NotApplicable: {0})".format(str(self.obj))
    __repr__=__str__

class Affirmative(ExplainedAnswer):
    def __init__(self, explanation="no reason given"):
        assert isinstance(explanation, basestring)
        self.obj = True
        self.explanation = explanation

    def __nonzero__(self):
        return True

class NegativeAnswer(ExplainedAnswer):
    def __init__(self, explanation="no reason given"):
        assert isinstance(explanation, basestring)
        self.obj = False
        self.explanation = explanation
Negative = NegativeAnswer
