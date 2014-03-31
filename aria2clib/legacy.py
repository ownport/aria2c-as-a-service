#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# aria2c python library for JSON-RPC
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

import re
import json
import time
import base64
import urllib2
import httplib

from pprint import pprint

JSON_RPC_VERSION = '2.0'
ARIA2C_PREFIX = 'aria2'
GLOBAL_STATS_FIELDS = [u'downloadSpeed', u'numActive', u'numStopped', u'numWaiting', u'uploadSpeed']
GLOBAL_OPTION_FIELDS = [
    u'follow-torrent', u'help', u'uri-selector', u'enable-rpc', u'enable-http-keep-alive',
    u'max-overall-download-limit', u'no-conf', u'bt-min-crypto-level', u'max-concurrent-downloads',
    u'conf-path', u'max-download-result', u'no-netrc', u'peer-id-prefix', u'stop', u'max-resume-failure-tries',
    u'async-dns', u'force-save', u'daemon', u'max-overall-upload-limit', u'continue', u'enable-mmap', 
    u'timeout', u'rpc-passwd', u'max-download-limit', u'no-file-allocation-limit', u'dir', u'enable-dht6',
    u'allow-piece-length-change', u'bt-tracker-connect-timeout', u'show-console-readout', u'human-readable',
    u'bt-stop-timeout', u'seed-ratio', u'use-head', u'follow-metalink', u'show-files', u'listen-port',
    u'dht-listen-port', u'retry-wait', u'file-allocation', u'connect-timeout', u'bt-request-peer-speed-limit',
    u'quiet', u'log-level', u'rpc-max-request-size', u'bt-enable-lpd', u'bt-max-peers', u'auto-file-renaming',
    u'ftp-type', u'rpc-secure', u'metalink-preferred-protocol', u'user-agent', u'disable-ipv6', u'http-no-cache',
    u'max-connection-per-server', u'remote-time', u'log', u'bt-metadata-only', u'piece-length', u'rpc-listen-port',
    u'disk-cache', u'conditional-get', u'console-log-level', u'ftp-reuse-connection', u'dry-run', 
    u'rpc-listen-all', u'event-poll', u'allow-overwrite', u'remove-control-file', u'truncate-console-readout',
    u'max-file-not-found', u'rpc-user', u'deferred-input', u'rpc-allow-origin-all', u'dht-message-timeout',
    u'check-certificate', u'http-auth-challenge', u'realtime-chunk-checksum', u'always-resume', 
    u'save-session-interval', u'reuse-uri', u'http-accept-gzip', u'bt-remove-unselected-file', u'max-upload-limit',
    u'rpc-save-upload-metadata', u'bt-require-crypto', u'check-integrity', u'proxy-method', u'ca-certificate',
    u'bt-tracker-timeout', u'max-tries', u'ftp-pasv', u'bt-tracker-interval', u'enable-dht', u'split',
    u'min-split-size', u'stream-piece-selector', u'bt-save-metadata', u'metalink-enable-unique-protocol',
    u'download-result', u'dht-file-path6', u'hash-check-only', u'server-stat-timeout', u'enable-peer-exchange',
    u'enable-http-pipelining', u'summary-interval', u'bt-max-open-files', u'dht-file-path', u'auto-save-interval',
    u'parameterized-uri', u'bt-hash-check-seed', u'bt-seed-unverified', u'lowest-speed-limit',
    u'on-download-complete', u'on-download-error', u'on-download-pause', u'on-download-start', u'on-download-stop',
]


class LegacyClient(object):
    
    def __init__(self, client_id=None, uri=None, username=None, password=None):
        '''
        - client_id - An identifier established by the Client that MUST contain a String, Number, or NULL value 
        if included. If it is not included it is assumed to be a notification. The value SHOULD normally not be 
        Null and Numbers SHOULD NOT contain fractional parts
        
        - uri = host an port of aria2c server in the format `http://<host>:<port>`
        '''
        self._json_rpc_version = JSON_RPC_VERSION
        self._aria2c_prefix = ARIA2C_PREFIX

        if not client_id:
            raise RuntimeError('client_id is not defined')
        self.client_id = client_id
            
        if not uri:
            raise RuntimeError('URI is not defined')

        if not isinstance(uri, (str, unicode)):
            raise RuntimeError('Incorrect URI type: %s' % type(uri))
        
        elif not re.match(r'http://.+?:\d+', uri):
            raise RuntimeError('incorrect URI format: %s' % uri)
        self.uri = uri + '/jsonrpc'
        
        self.username = username
        self.password = password
            

    # IMPLEMENTED IN SIMPLE_CLIENT
    def send_request(self, command, parameters=[]):
        ''' send JSON-RPC request
        '''

        jsonreq = json.dumps({
                    'jsonrpc':  self._json_rpc_version, 
                    'id':       self.client_id, 
                    'method':   '%s.%s' % (self._aria2c_prefix, command),
                    'params':   parameters,
        })
        
        request = urllib2.Request(self.uri, jsonreq)
        if self.username and self.password:
            base64string = base64.encodestring('%s:%s' % (self.username, self.password)).replace('\n', '')
            request.add_header('Authorization', 'Basic %s' % base64string)

        c = urllib2.urlopen(request)
        response = json.loads(c.read())
        return response
        

    # IMPLEMENTED IN SIMPLE_CLIENT
    def add_uri(self, uris, options=[], position=None):
        ''' This method adds new HTTP(S)/FTP/BitTorrent Magnet URI. 
        
        - uris is of type array and its element is URI which is of type string. For BitTorrent Magnet URI, uris must 
        have only one element and it should be BitTorrent Magnet URI. URIs in uris must point to the same file. If 
        you mix other URIs which point to another file, aria2 does not complain but download may fail. 
        
        - options is of type struct and its members are a pair of option name and value.
        
        - If position is given as an integer starting from 0, the new download is inserted at position in the waiting 
        queue. If position is not given or position is larger than the size of the queue, it is appended at the end of 
        the queue. 
        
        This method returns GID of registered download. GID calculates as md5 hash of first uri
        '''
        # TODO support few uris to the same file
        
        if isinstance(uris, (unicode, str)):
            uris = [uris]

        return self.send_request('addUri', [uris, options])    


    def remove(self, gid):
        ''' This method removes the download denoted by gid. gid is of type string. If specified download is in 
        progress, it is stopped at first. The status of removed download becomes removed. This method returns GID 
        of removed download.
        '''
        
        return self.send_request('remove', [gid,])

    
    def force_remove(self, gid):
        '''This method removes the download denoted by gid. This method behaves just like aria2.remove() except 
        that this method removes download without any action which takes time such as contacting BitTorrent 
        tracker
        '''
        return self.send_request('forceRemove', [gid,])
        

    def pause(self, gid):
        ''' This method pauses the download denoted by gid. gid is of type string. The status of paused download 
        becomes paused. If the download is active, the download is placed on the first position of waiting queue. 
        As long as the status is paused, the download is not started. To change status to waiting, use aria2.unpause() 
        method. This method returns GID of paused download.
        '''
        return self.send_request('pause', [gid,])
        

    def pause_all(self):
        ''' This method is equal to calling aria2.pause() for every active/waiting download. 
        This methods returns OK for success.
        '''
        return self.send_request('pauseAll')


    def force_pause(self, gid):
        ''' This method pauses the download denoted by gid. This method behaves just like aria2.pause() except that 
        this method pauses download without any action which takes time such as contacting BitTorrent tracker.
        '''
        return self.send_request('forcePause', [gid,])
        
    
    def force_pause_all(self):
        ''' This method is equal to calling aria2.forcePause() for every active/waiting download. 
        This methods returns OK for success.
        '''
        return self.send_request('forcePauseAll')


    def unpause(self, gid):
        ''' This method changes the status of the download denoted by gid from paused to waiting. This makes 
        the download eligible to restart. gid is of type string. This method returns GID of unpaused download.
        '''
        return self.send_request('unpause', [gid,])


    def unpause_all(self):
        ''' This method is equal to calling aria2.unpause() for every active/waiting download. 
        This methods returns OK for success.
        '''
        return self.send_request('unpauseAll')
                
    # IMPLEMENTED IN SIMPLE_CLIENT
    def tell_status(self, gid, keys=[]):
        ''' This method returns download progress of the download denoted by gid. 
        
        - gid is of type string. 
        
        - keys is array of string. If it is specified, the response contains only keys in keys array. If keys is 
        empty or not specified, the response contains all keys. This is useful when you just want specific keys and 
        avoid unnecessary transfers.
        
        the list of keys is available by http://aria2.sourceforge.net/manual/en/html/aria2c.html#aria2.tellStatus
        '''

        return self.send_request('tellStatus', [gid, keys])    

    
    def get_uris(self, gid):
        ''' This method returns URIs used in the download denoted by gid. gid is of type string. The response is of 
        type array and its element is of type struct and it contains following keys. The value type is string.
        
        uri:    URI
        status: 'used' if the URI is already used. 'waiting' if the URI is waiting in the queue.
        '''
        return self.send_request('getUris', [gid,])    
        

    def get_files(self, gid):
        ''' This method returns file list of the download denoted by gid. gid is of type string. The response is of 
        type array and its element is of type struct and it contains following keys. The value type is string.

        - index:    Index of file. Starting with 1. This is the same order with the files in multi-file torrent.
        - path:     File path.
        - length:   File size in bytes.
        - completedLength: Completed length of this file in bytes. Please note that it is possible that sum of 
        completedLength is less than completedLength in aria2.tellStatus() method. This is because completedLength 
        in aria2.getFiles() only calculates completed pieces. On the other hand, completedLength in aria2.tellStatus() 
        takes into account of partially completed piece.
        - selected: true if this file is selected by --select-file option. If --select-file is not specified or this is 
        single torrent or no torrent download, this value is always true. Otherwise false.
        - uris: Returns the list of URI for this file. The element of list is the same struct used in aria2.getUris() method.
        '''
        return self.send_request('getFiles', [gid,])    
        

    def get_servers(self, gid):
        '''This method returns currently connected HTTP(S)/FTP servers of the download denoted by gid. gid is of type 
        string. The response is of type array and its element is of type struct and it contains following keys. 
        The value type is string.

        - index: Index of file. Starting with 1. This is the same order with the files in multi-file torrent.
        - servers: The list of struct which contains following keys.
        - uri: URI originally added.
        - currentUri: This is the URI currently used for downloading. If redirection is involved, currentUri and uri may differ.
        - downloadSpeed: Download speed (byte/sec)
        '''
        return self.send_request('getServers', [gid,])    
        
    
    # IMPLEMENTED IN SIMPLE_CLIENT
    def tell_active(self, keys=[]):
        ''' This method returns the list of active downloads. The response is of type array and its element is the 
        same struct returned by aria2.tellStatus() method. For keys parameter, 
        please refer to aria2.tellStatus() method.
        '''
        return self.send_request('tellActive', [keys])    


    # IMPLEMENTED IN SIMPLE_CLIENT
    def tell_waiting(self, offset=0, num=100, keys=[]):
        ''' This method returns the list of waiting download, including paused downloads. 
        
        - offset is of type integer and specifies the offset from the download waiting at the front. 
        - num is of type integer and specifies the  number of downloads to be returned. 
        - For keys parameter, please refer to aria2.tellStatus() method.

        If offset is a positive integer, this method returns downloads in the range of [offset, offset + num).

        offset can be a negative integer. offset == -1 points last download in the waiting queue and 
        offset == -2 points the download before the last download, and so on. The downloads in the response are 
        in reversed order.

        For example, imagine that three downloads "A","B" and "C" are waiting in this order. aria2.tellWaiting(0, 1) 
        returns ["A"]. aria2.tellWaiting(1, 2) returns ["B", "C"]. aria2.tellWaiting(-1, 2) returns ["C", "B"].

        The response is of type array and its element is the same struct returned by aria2.tellStatus() method.
        '''
        return self.send_request('tellWaiting', [offset, num, [keys]])    


    # IMPLEMENTED IN SIMPLE_CLIENT
    def tell_stopped(self, offset=0, num=100, keys=[]):
        ''' This method returns the list of stopped download. offset is of type integer and specifies the offset 
        from the oldest download. num is of type integer and specifies the number of downloads to be returned. 
        For keys parameter, please refer to aria2.tellStatus() method.

        offset and num have the same semantics as aria2.tellWaiting() method.

        The response is of type array and its element is the same struct returned by aria2.tellStatus() method.
        '''
        return self.send_request('tellStopped', [offset, num, [keys]])    
                
    
    # IMPLEMENTED IN SIMPLE_CLIENT
    def get_option(self, gid):
        ''' This method returns options of the download denoted by gid. The response is of type struct. Its key is 
        the name of option. The value type is string. Note that this method does not return options which have no 
        default value and have not been set by the command-line options, configuration files or RPC methods.
        '''
        return self.send_request('getOption', [gid,])    


    # IMPLEMENTED IN SIMPLE_CLIENT
    def get_global_stats(self):
        ''' This method returns global statistics such as overall download and upload speed. The response is of 
        type struct and contains following keys. The value type is string.
        
        downloadSpeed: Overall download speed (byte/sec).
        uploadSpeed: Overall upload speed(byte/sec).
        numActive: The number of active downloads.
        numWaiting: The number of waiting downloads.
        numStopped: The number of stopped downloads.
        '''
        return self.send_request('getGlobalStat')

    
    # IMPLEMENTED IN SIMPLE_CLIENT
    def get_global_option(self):
        ''' This method returns global options. The response is of type struct. Its key is the name of option. 
        The value type is string. Note that this method does not return options which have no default value and 
        have not been set by the command-line options, configuration files or RPC methods. Because global options 
        are used as a template for the options of newly added download, the response contains keys returned by 
        self.getOption() method.
        '''
        return self.send_request('getGlobalOption')


    def purge_download_result(self):
        ''' This method purges completed/error/removed downloads to free memory. This method returns OK.
        '''
        return self.send_request('purgeDownloadResult')


    def remove_download_result(self, gid):
        ''' This method removes completed/error/removed download denoted by gid from memory. 
        This method returns OK for success.
        '''
        return self.send_request('removeDownloadResult', [gid,])    


    # IMPLEMENTED IN SIMPLE_CLIENT
    def get_version(self):
        ''' This method returns version of the program and the list of enabled features. 
        The response is of type struct and contains following keys.

        - version: Version number of the program in string.
        - enabledFeatures: List of enabled features. Each feature name is of type string.
        '''
        return self.send_request('getVersion')

    
    # IMPLEMENTED IN SIMPLE_CLIENT
    def get_session_info(self):
        ''' This method returns session information. 
        The response is of type struct and contains following key.

        - sessionId: Session ID, which is generated each time when aria2 is invoked.
        '''
        return self.send_request('getSessionInfo')


    def shutdown(self):
        ''' This method shutdowns aria2. This method returns OK.
        '''
        return self.send_request('shutdown')


    def forceShutdown(self):
        ''' This method shutdowns aria2. This method behaves like  aria2.shutdown() except that any actions 
        which takes time such as contacting BitTorrent tracker are skipped. This method returns OK.
        '''
        return self.send_request('forceShutdown')

    
