""" tests/test_inspect.py
"""
from unittest import TestCase

from goulash._inspect import getcaller

class TestClass(object):
    def method(self):
        return getcaller()

class TestInspect(TestCase):
    def test_getcaller(self):
        result = getcaller()
        self.assertEqual(
            set(result.keys()),
            set(['class', 'globals', 'locals',
                 'file', 'func_name', 'self', 'func']))

    def test_getcaller2(self):
        tmp = TestClass().method()
        self.assertEqual(tmp['class'], self.__class__)
        self.assertEqual(tmp['file'], __file__)
        self.assertEqual(tmp.self, self)
        self.assertEqual(tmp.func, self.test_getcaller2)
