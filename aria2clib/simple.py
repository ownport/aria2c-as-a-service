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

from hashlib import md5

from legacy import LegacyClient


class SimpleClient(object):
    ''' SimpleClient
    '''
    def __init__(self, client_id=None, uri=None, username=None, password=None):
        ''' __init__
        '''
        if not client_id:
            raise RuntimeError('client_id is not defined')
        self._client = LegacyClient(client_id=client_id, uri=uri, username=username, password=password)
    
    
    def _make_gid(self, url):
        ''' return gid as hash of url
        '''
        return md5(url).hexdigest()
        
    
    def get(self, gid=[]):
        ''' get status of files
        '''
        return []
    
    
    def put(self, url, params=[], pause=False):
        ''' put url(s) to queue for downloading
        
        if pause=True, If the download is active, the download is placed on the first position of waiting queue. 
        As long as the status is paused, the download is not started. To continue download, call put() with pause=False
        for those urls
        '''
        
        result = self._client.add_uri(url, params)        

        return result
    
    
    def delete(self, url, force=False):
        ''' delete file(s) by url(s)
        
        - gid can be as single value or a list of gids
        
        - force=True,  this method removes download without any action which takes time such as contacting 
        BitTorrent tracker
        - force=Falce (default), it is stopped download at first than download becomes removed.
        '''
        urls = list()
       
        # handle list or single url(s)       
        if isinstance(url, (string, unicode, int)):
            urls.append(url)
        else:
            urls.extend(url)
        
        for url in urls:
            if force:
                print self._client.force_remove(url)
                continue
            print self._client.remove(url)


    def stats(self):
        ''' return aria2c stats
        '''
        
        return []            

        
