#!/usr/bin/env python
#
#   test server
#
import os
import bottle
import logging

from datetime import datetime

STATIC_PATH = os.path.join( os.path.dirname(os.path.abspath(__file__)), 'static')

# monkey patching for BaseHTTPRequestHandler.log_message
def log_message(obj, format, *args):
    logging.debug("%s - - [%s] %s" % (obj.address_string(), obj.log_date_time_string(), format%args))
    

@bottle.route('/static/<filename>')
def handle_static(filename):
    return bottle.static_file(filename, root=STATIC_PATH)


if __name__ == "__main__":

    import sys
    
    if len(sys.argv) == 2 and sys.argv[1].startswith('--logfile='):

        logfile = sys.argv[1].split('=')[1]
        logging.basicConfig(
                    filename=logfile, 
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG
        )
        from BaseHTTPServer import BaseHTTPRequestHandler
        BaseHTTPRequestHandler.log_message = log_message    

    bottle.run(host='0.0.0.0', port=8080, debug=True)


