import time
import unittest

from pprint import pprint
from urllib2 import HTTPError
from aria2clib import SimpleClient
from aria2clib import GLOBAL_STATS_FIELDS
from aria2clib import GLOBAL_OPTION_FIELDS


class SimpleClientTest(unittest.TestCase):

    def test_client_misconfiguration(self):
        ''' test_client_misconfiguration
        '''
        self.assertRaises(RuntimeError, SimpleClient, )
        self.assertRaises(RuntimeError, SimpleClient, 'aria2clib-client')
        self.assertRaises(RuntimeError, SimpleClient, 'aria2clib-client', 'localhost')
        self.assertRaises(RuntimeError, SimpleClient, 'aria2clib-client', 'localhost:6800')
        self.assertRaises(RuntimeError, SimpleClient, 'aria2clib-client', 'http:localhost:6800')
        self.assertRaises(RuntimeError, SimpleClient, 'aria2clib-client', ['http:localhost:6800'])


    def test_create_client_without_auth(self):
        ''' test_create_client_without_auth
        '''
        client = SimpleClient('aria2clib-client', 'http://localhost:6800')
        self.assertRaises(HTTPError, client.put, ('http://localhost:8080/static/sc.test_create_client_without_auth'))


    def test_incorrect_uri_type(self):
        ''' test_incorrect_uri_type
        '''
        client = SimpleClient('aria2clib-client', 'http://localhost:6800')
        self.assertRaises(RuntimeError, client.put, ({}))
        
        
    def test_create_client_with_auth(self):
        ''' test_create_client_without_auth
        '''
        client = SimpleClient('aria2clib-client', 'http://localhost:6800', 'aria2c', 'aria2c')
        response = client.put('http://localhost:8080/static/sc.test_create_client_with_auth')
        self.assertEqual(response, [u'233600615c1e6308',])


    def test_get_put_delete_one_url(self):
        ''' test_get_put_delete_one_url
        '''
        client = SimpleClient('aria2clib-client', 'http://localhost:6800', 'aria2c', 'aria2c')
        response = client.put('http://localhost:8080/static/sc.test_get_put_delete_one_url')
        self.assertEqual(response, [u'e99400b47fd00b83'])

        response = client.get(u'e99400b47fd00b83')
        if len(response) < 1:
            raise RuntimeError('len(response) < 1, len(): %d' % len(response))

        response = client.delete(u'e99400b47fd00b83')
        self.assertEqual(response, [(u'e99400b47fd00b83', u'OK')]) 

        
    def test_get_put_delete_many_urls(self):
        ''' test_get_put_delete_many_urls
        '''
        gids = [u'851ee2c323baaa8b', u'150ba9ab5d31ff46', u'340d520c4ea83c91']
        client = SimpleClient('aria2clib-client', 'http://localhost:6800', 'aria2c', 'aria2c')
        response = client.put([
            'http://localhost:8080/static/sc.test_get_put_delete_many_urls.1',
            'http://localhost:8080/static/sc.test_get_put_delete_many_urls.2',
            'http://localhost:8080/static/sc.test_get_put_delete_many_urls.3',
        ])
        self.assertEqual(response, gids)

        response = client.get(gids)
        if len(response) < 3:
            raise RuntimeError('len(response) < 3, len(): %d' % len(response))
        
        response = client.get()
        if len(response) < 3:
            raise RuntimeError('len(response) < 3, len(): %d' % len(response))

        # TODO delete many
        response = client.delete([u'851ee2c323baaa8b', u'150ba9ab5d31ff46'])
        self.assertEqual(response, [(u'851ee2c323baaa8b', u'OK'), (u'150ba9ab5d31ff46', u'OK')]) 

        response = client.delete(u'340d520c4ea83c91', force=True)
        self.assertEqual(response, [(u'340d520c4ea83c91', u'OK'),]) 


    def test_stats(self):
        ''' test stats
        '''
        client = SimpleClient('aria2clib-client', 'http://localhost:6800', 'aria2c', 'aria2c')
        stats = client.stats()
        self.assertEqual(set(stats['version'].keys()), set([u'version', u'enabledFeatures']))
        self.assertEqual(set(stats['session_info'].keys()), set([u'sessionId']))
        self.assertEqual(set(stats['global_stats'].keys()).issubset(set(GLOBAL_STATS_FIELDS)), True)
        self.assertEqual(set(stats['global_option'].keys()).issubset(set(GLOBAL_OPTION_FIELDS)), True)

        
