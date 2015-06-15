""" test_settings

    TODO: test command line parsing
"""
import unittest
import mock
from argparse import ArgumentParser
from goulash.python import dirname, opj
from goulash.settings import Settings, SettingsError

this_dir = dirname(__file__)

class TestSettings(unittest.TestCase):

    def setUp(self):
        self.settings = Settings(opj(this_dir, 'test.ini'), use_argv=False)

    def test_get_parser(self):
        parser = self.settings.get_parser()
        self.assertTrue(isinstance(parser, ArgumentParser))

    def test_get_setting(self):
        self.assertEqual(self.settings.get_setting('section1.undefined'), None)
        self.assertEqual(
            self.settings.get_setting(
                'section1.undefined', default='default'),
            'default')
        self.assertEqual(self.settings.get_setting('section1.var1'), 'val1')
        self.assertEqual(self.settings.get_setting('section2.var1'), 'val1')
        self.assertRaises(
            SettingsError,
            lambda: self.settings.get_setting(
                'section1.undefined', insist=True),)

    def test_get_section(self):
        self.assertEqual(
            self.settings['section1'],
            self.settings.get_section('section1'))
        self.assertTrue(
            str(type(self.settings.get_section('section1'))),
            'Section')
        self.assertRaises(
            SettingsError,
            lambda: self.settings.get_section(
                'undefined', insist=True),)

    def test_implied_dynamic_keys(self):
        self.assertTrue('user' in self.settings)

    def test_dict_compat(self):
        self.assertTrue('section1' in self.settings)
        self.assertTrue(dict(self.settings['section1']))
        self.assertTrue(isinstance(self.settings.keys(), list))
