""" test_os """

import unittest

from goulash._os import file_age_in_seconds, get_mounts_by_type

class TestOS(unittest.TestCase):

    def setUp(self):
        pass

    def test_file_age_in_seconds(self):
        # no mock for this yet and it's pretty simple,
        # so we just exercise the code.
        file_age_in_seconds(__file__)
        self.assertEqual(file_age_in_seconds('--doesnt-exist--'), None)

    def test_get_mounts(self):
        tmp = get_mounts_by_type('proc')
        for mp in tmp:
            self.assertTrue('name' in mp)
            self.assertTrue('mount_point' in mp)
