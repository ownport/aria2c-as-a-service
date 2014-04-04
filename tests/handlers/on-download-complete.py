#!/usr/bin/env python
#
#   aria2c event handler `on-download-comleted`
#

import os
import sys
import json

from hashlib import md5, sha1
#from aria2clib import SimpleClient


def calc_hash(hash_func, filename):
    ''' return file checksum calculated by hash_func
    '''
    with open(filename, 'rb') as fh:
        while True:
            data = fh.read(8192)
            if not data:
                break
            hash_func.update(data)
    return hash_func.hexdigest()


def update_meta(gid, path):
    ''' update file metadata
    '''
    metafile = path + '.meta'
    if os.path.exists(metafile):
        metadata = json.load(open(metafile))
    else:
        metadata = dict()
        
    metadata[u'gid'] = unicode(gid)
    try:
        metadata[u'md5'] = unicode(calc_hash(md5(), path))
        metadata[u'sha1'] = unicode(calc_hash(sha1(), path))
    except IOError:
        print >> sys.stderr, 'Error! File not found, %s' % path
        sys.exit(1)
        
    json.dump(metadata, open(metafile, 'wb'))


def main(client, gid, files, path):

    update_meta(gid, path)


