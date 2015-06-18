""" tests/test_projects
"""
import os
import unittest

from fabric import api
from goulash.projects import project_search

class TestProjects(unittest.TestCase):

    def setUp(self):
        self.fake_project_dir = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                'fake_project'))
        assert os.path.exists(self.fake_project_dir)

    def test_psearch_implied_arg(self):
        os.chdir(os.path.join(self.fake_project_dir, 'foo','bar','baz'))
        actual = project_search('project.json')
        expected = os.path.abspath(
            os.path.join(self.fake_project_dir, 'project.json'))
        self.assertEqual(actual,expected)

    def test_psearch_explicit_arg(self):
        tmp = os.path.join(self.fake_project_dir, 'foo','bar','baz')
        actual = project_search('project.json', tmp)
        expected = os.path.abspath(
            os.path.join(self.fake_project_dir, 'project.json'))
        self.assertEqual(actual, expected)

if __name__=='__main__':
    unittest.main()
