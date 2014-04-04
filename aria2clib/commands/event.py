import imp
import sys

from simple_api import SimpleClient

from command import Aria2cCommand, UsageError


class Command(Aria2cCommand):

    name = 'event'

    def short_desc(self):

        return "aria2c event handler"

        
    def add_options(self, parser):
        
        Aria2cCommand.add_options(self, parser)
        parser.add_argument("--handler", type=str, help="handler module")
        parser.add_argument("--gid", type=str, help="GID")
        parser.add_argument("--files", type=str, help="the number of files")
        parser.add_argument("--path", type=str, help="path")
    

    def process_options(self, args):
        
        Aria2cCommand.process_options(self, args)

        if args.gid:
            self.gid = args.gid
        else:
            raise UsageError('Missed --gid parameter')

        if args.files:
            self.files = args.files
        else:
            raise UsageError('Missed --files parameter')

        if args.path:
            self.path = args.path
        else:
            raise UsageError('Missed --path parameter')

        if args.handler:
            self.handler = args.handler
        else:
            raise UsageError('Missed --handler parameter')

    def run(self):

        try:
            handler = imp.load_source('handler', self.handler)
        except IOError:
            print >> sys.stderr, 'Error! No handler module found, %s' % self.handler
            sys.exit(1)
            
        handler.main(SimpleClient, self.gid, self.files, self.path)
        
