
class UsageError(Exception):
    """To indicate a command-line usage error
    """
    def __init__(self, *a, **kw):
    
        self.print_help = kw.pop('print_help', True)
        super(UsageError, self).__init__(*a, **kw)


class Aria2cCommand(object):

    def __init__(self):
        
        self.name = 'Aria2cCommand'
        self.exitcode = 0
        self.settings = dict()
        
        self.logger = None
        self.settings['LOG_LEVEL'] = 'INFO'


    def syntax(self):
        """ Command syntax (preferably one-line). Do not include command name.
        """
        return ""


    def short_desc(self):
        """ A short description of the command
        """
        return ""


    def long_desc(self):
        """ A long description of the command. Return short description when not
        available. It cannot contain newlines, since contents will be formatted
        by argparse which removes newlines and wraps text.
        """
        return self.short_desc()


    def help(self):
        """ An extensive help for the command. It will be shown when using the
        "help" command. It can contain newlines, since not post-formatting will
        be applied to its contents.
        """
        return self.long_desc()


    def add_options(self, parser):
        """ Populate option parse with options available for this command
        """
        parser.add_argument("--logfile", metavar="FILE", type=str, 
            help="log file. if omitted stderr will be used")
        parser.add_argument("-L", "--loglevel", metavar="LEVEL", type=str, 
            default=None, help="log level (default: INFO)")

    def process_options(self, args):

        if args.loglevel:
            self.settings['LOG_LEVEL'] = args.loglevel
        
        if args.logfile:
            self.settings['LOG_FILE'] = args.logfile
            self.logger = log.get_file_logger(self.name, self.settings['LOG_LEVEL'], args.logfile)


    def run(self):
        """ Entry point for running commands
        """
        raise NotImplementedError
        
