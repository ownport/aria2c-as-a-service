import json
from pprint import pprint

from simple_api import SimpleClient

from command import Aria2cCommand, UsageError


class Command(Aria2cCommand):

    name = 'client'

    def short_desc(self):

        return "operate with aria2c daemon via Simple Client API"

        
    def add_options(self, parser):
        
        Aria2cCommand.add_options(self, parser)
        parser.add_argument("--client_id", type=str, help="client id")
        parser.add_argument("--uri", type=str, help="URI to aria2c daemon")
        parser.add_argument("--username", type=str, help="aria2c daemon username")
        parser.add_argument("--password", type=str, help="aria2c daemon password")
        
        parser.add_argument("--put", type=str, 
                            help="put task specified by simple url " + \
                            "or parameters in JSON format " + \
                            "or reference to JSON file (file:<filename.json>)")
        parser.add_argument("--get", type=str, 
                            help="get details by one or several GIDs separated by ',' or 'all'")
        parser.add_argument("--delete", type=str, 
                            help="delete task(s) by one or several GIDs separated by ','")
        parser.add_argument("--stats", action="store_true", 
                            help="print aria2c info")
    

    def process_options(self, args):
        
        Aria2cCommand.process_options(self, args)

        if args.client_id:
            self.client_id = args.client_id
        else:
            raise UsageError('Missed --client_id parameter')

        if args.uri:
            self.uri = args.uri
        else:
            raise UsageError('Missed --uri parameter')

        self.username = args.username
        self.password = args.password
        self.command_put = args.put
        self.command_get = args.get
        self.command_delete = args.delete
        self.command_stats = args.stats
        

    def run(self):

        client = SimpleClient(client_id=self.client_id, uri=self.uri, username=self.username, password=self.password)
        
        if self.command_stats:
            pprint(client.stats())

        elif self.command_get:
            if self.command_get == 'all':
                pprint(client.get())
            else:
                pprint(client.get(self.command_get.split(',')))

        elif self.command_put:
            # URL
            if self.command_put.startswith('http://'):
                print client.put(self.command_put)
            
            # file
            elif self.command_put.startswith('file:'):
                with open(self.command_put.replace('file:', '')) as source:
                    input_params = json.loads(source.read())
                    urls    = input_params.get('urls', [])
                    params  = input_params.get('params', {})
                    pause   = input_params.get('pause', False)
                    pprint(client.put(urls, params, pause))
            
            # parameters in JSON
            else:
                input_params = json.loads(self.command_put)
                urls    = input_params.get('urls', [])
                params  = input_params.get('params', {})
                pause   = input_params.get('pause', False)
                pprint(client.put(urls, params, pause))

        elif self.command_delete:
            pprint(client.delete(self.command_delete.split(',')))
        
        else:
            raise RuntimeError('Unknown command or no command defined')    
            
        
