#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
from urllib2 import HTTPError

from legacy import LegacyClient


class SimpleClient(object):
    ''' SimpleClient
    '''
    def __init__(self, client_id=None, uri=None, username=None, password=None):
        ''' __init__
        '''
        self._client = LegacyClient(client_id=client_id, uri=uri, username=username, password=password)
    
    
    def _calc_gid(self, url):
        ''' return gid as hash of url
        
        Hash calculated based on md5 algorithm with length limitation up to 16 characters
        '''
        return md5(url).hexdigest()[:16]
        

    def _queues_files(self):
        ''' return the list of active, waiting, stopped queues
        
        flatting `uris` fields 
        '''
        result = list()
        
        queues = (
            (u'active', self._client.tell_active()), 
            (u'waiting', self._client.tell_waiting()),
            (u'stopped', self._client.tell_stopped()),
        )
        
        for (status, queue) in queues:
            queue = queue.get('result', [])
            for f in queue:
                for file_info in f.get('files', []):
                    file_info[u'status'] = status
                    file_info = self._flatting_file_info(file_info)
                    file_info[u'gids'] = [self._calc_gid(u) for u in file_info[u'uris']]
                result.append(file_info)
                    
        return result


    def _flatting_file_info(self, info):
        ''' return flatted file info
        '''
        uris = dict()
        for uri in info['uris']:
            if uri[u'uri'] not in uris:
                uris[uri[u'uri']] = [uri['status'],]
            else:
                uris[uri[u'uri']].append(uri['status'])
        info[u'uris'] = uris
        return info 

    
    def _update_urls(self, url):
        ''' return the list of pairs: url and GID (md5 hash of url)
        
        The GID must be hex string of 16 characters, thus [0-9a-zA-Z] are allowed and leading zeros must not be 
        stripped. The GID all 0 is reserved and must not be used. The GID must be unique, otherwise error is 
        reported and the download is not added. 
        '''
        urls = list()
        
        if isinstance(url, (unicode, str)):
            urls.append(url)
        elif isinstance(url, (list, tuple)):
            urls.extend(url)
        else:
            raise RuntimeError('Incorrect url type: %s' % type(url))

        urls = [(u, self._calc_gid(u)) for u in urls]
        return urls        

    
    def get(self, gid=[]):
        ''' get status of files
        '''
        files = self._queues_files()
        if isinstance(gid, (unicode, str)):
            return [f for f in files if gid in f[u'gids']]
            
        elif isinstance(gid, (list, tuple)) and gid:
            result = list()
            for f in files:
                result.extend([f for g in gid if g in f[u'gids']])
            return result
        else:
            return files
    
    
    def put(self, urls, params={}, pause=False):
        ''' put url(s) to queue for downloading
        
        if pause=True, If the download is active, the download is placed on the first position of waiting queue. 
        As long as the status is paused, the download is not started. To continue download, call put() with pause=False
        for those urls
        '''
        
        result = list()
        for u in self._update_urls(urls):    
            params['gid'] = u[1]
            response = self._client.add_uri(u[0], params)
            result.append(response.get('result', None))
        return result
    
    
    def delete(self, gid, force=False):
        ''' delete file(s) by gid(s)
        
        - gid can be as single value or a list of gids
        
        - force=True,  this method removes download without any action which takes time such as contacting 
        BitTorrent tracker
        - force=Falce (default), it is stopped download at first than download becomes removed.
        '''
        gids = list()
       
        # handle list or single url(s)       
        if isinstance(gid, (str, unicode)):
            gids.append(gid)
        else:
            gids.extend(gid)

        result = list()
        for gid in gids:
            if force:
                try:
                    response = self._client.force_remove(gid).get('result', None)
                except HTTPError:
                    pass
            else:        
                try:
                    response = self._client.remove(gid).get('result', None)
                except HTTPError:
                    pass
            result.append((gid, self._client.remove_download_result(gid).get('result', None)))
        return result


    def stats(self):
        ''' return aria2c stats
        '''
        response = {}
        response['version'] = self._client.get_version().get('result', None)
        response['session_info'] = self._client.get_session_info().get('result', None)
        response['global_stats'] = self._client.get_global_stats().get('result', None)
        response['global_option'] = self._client.get_global_option().get('result', None)
        return response 

        
