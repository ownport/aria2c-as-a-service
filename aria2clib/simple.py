#!/usr/bin/env python
#
# simplified aria2c python library for JSON-RPC
#
# aria2 provides JSON-RPC over HTTP and XML-RPC over HTTP and they basically have the same functionality. 
# aria2 also provides JSON-RPC over WebSocket. JSON-RPC over WebSocket uses same method signatures and 
# response format with JSON-RPC over HTTP, but it additionally has server-initiated notifications. 
#
# The request path of JSON-RPC interface (for both over HTTP and over WebSocket) is /jsonrpc. The request 
# path of XML-RPC interface is /rpc.
#
# The WebSocket URI for JSON-RPC over WebSocket is ws://HOST:PORT/jsonrpc. If you enabled SSL/TLS encryption, 
# use wss://HOST:PORT/jsonrpc instead.
#
#
# Links
# - [JSON-RPC 2.0 Specification](http://www.jsonrpc.org/specification)
#

from legacy import LegacyClient


class SimpleClient(object):
    ''' SimpleClient
    '''
    def __init__(self, client_id=None, uri=None, username=None, password=None):
        ''' __init__
        '''
        self._client = Aria2cJsonClient()
    
    
    def get(self, gid=[]):
        ''' get status of files
        '''
        return []
    
    
    def put(self, url, params={}):
        ''' put url(s) to queue for downloading
        '''
        return []
    
    
    def delete(self, gid):
        ''' delete file(s) by gid(s)
        '''
        return []


    def stats(self):
        ''' return aria2c stats
        '''
        return []            

        
