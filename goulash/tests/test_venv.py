""" goulas.tests.test_venv
"""
import unittest

from goulash import venv
from goulash.python import dirname, opj

TEST_DIR = dirname(__file__)

class TestVenv(unittest.TestCase):

    def setUp(self):
        self.venv1 = opj(TEST_DIR, 'fake_venv')
        self.venv2 = opj(TEST_DIR, 'another_fake_virtual_env')

    def test_is_venv(self):
        self.assertTrue(venv.is_venv(self.venv1))

    def test_contains_venv(self):
        self.assertTrue(venv.contains_venv(TEST_DIR))

    def test_find_venvs(self):
        def report(*args):
            pass
        all_venvs = venv.find_venvs(
            TEST_DIR, report=report,max_venvs=5)
        self.assertEqual(all_venvs,[])
