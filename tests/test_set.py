""" test_set
"""
import unittest

from goulash.set import OrderedSet

class TestSet(unittest.TestCase):
    def setUp(self):
        self.s = OrderedSet('abracadaba')
        self.t = OrderedSet('simsalabim')

    def test_simple(self):
        expected = OrderedSet(['a', 'b', 'r', 'c', 'd', 's', 'i', 'm', 'l'])
        self.assertEqual(self.s | self.t, expected)
        expected = OrderedSet(['a','b'])
        self.assertEqual(self.s & self.t, expected)
        expected = OrderedSet(['r', 'c', 'd'])
        self.assertEqual(self.s - self.t, expected)
