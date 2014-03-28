import unittest

from aria2clib.simple import SimpleClient

class SimpleClientTest(unittest.TestCase):

    def test_client_misconfiguration(self):
        ''' test_client_misconfiguration
        '''
        self.assertRaises(RuntimeError, SimpleClient, )

