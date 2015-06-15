""" tests.test_fabric
"""

import unittest

from goulash import _fabric as gfabric

class TestFabric(unittest.TestCase):

    def test_qlocal(self):
        tmp = gfabric.qlocal('date', capture=True)
        self.assertTrue(tmp)
        self.assertTrue(tmp.succeeded)

    def test_has_bin(self):
        self.assertFalse(gfabric.has_bin('asdads-doesntexist-asdasda'))
        self.assertTrue(gfabric.has_bin('bash'))

    def test_require_bin(self):
        tmp = lambda: gfabric.require_bin('asdads-doesntexist-asdasda')
        self.assertRaises(gfabric.MissingSystemCommand, tmp)
        gfabric.require_bin('bash')

if __name__=='__main__':
    unittest.main()
