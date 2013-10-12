""" test_parsing:

      tests for goulash.parsing
"""

import unittest

from goulash.parsing import strip_tags

class TestStripTags(unittest.TestCase):
    def test_strip_tags(self):
        self.assertEqual(strip_tags("<a href=#>foo</a>"), 'foo')
