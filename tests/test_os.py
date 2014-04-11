""" test_os """

import unittest

from goulash import _os

class TestOS(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_mounts(self):
        tmp=_os.get_mounts_by_type('proc')
        from IPython import Shell; Shell.IPShellEmbed(argv=['-noconfirm_exit'])()
