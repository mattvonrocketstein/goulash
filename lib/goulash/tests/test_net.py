""" goulash.tests.test_net
"""

import mock
import unittest
from goulash import net as gnet

class TestAllStatic(unittest.TestCase):

    @mock.patch('socket.gethostbyname')
    def test_ipaddr_basic(self, get_host_by_name):
        get_host_by_name.return_value = 'fake'
        self.assertEqual(set(['fake']), gnet.ipaddr_basic())

    def test_is_port_open(self):
        self.fail('niy')

    def test_ipaddr_with_LAN(self):
        self.fail('niy')

    def test_ipaddr_hosts(self):
        self.fail('niy')
