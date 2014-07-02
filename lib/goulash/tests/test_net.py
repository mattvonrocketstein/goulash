""" goulash.tests.test_net
"""

import unittest
import mock
from goulash import net as gnet

class TestAllStatic(unittest.TestCase):

    @mock.patch('socket.gethostbyname')
    def test_ipaddr_basic(self, get_host_by_name):
        get_host_by_name.return_value = 'fake'
        self.assertEqual(set(['fake']), gnet.ipaddr_basic())
