from argparse import ArgumentParser
from urllib import parse
from urllib.parse import uses_fragment





class Args():
    def __init__(self):
        helpm  ='''
                -q, --query      - Dork that will be used in the search engine.
                -n, --number    - Number of results brought by the search engine.
                -s, --start-page - Home page of search results.
                -t, --timeout    - Timeout of requests.
                -ch, --checkform  - Check all form in url.

            Examples:
                python SqF.py --query 'home.php?id=10' --checkform --timeout 2.0
            '''
        self.parser = ArgumentParser(description='Process some integers.', usage=helpm)    

    def argparser(self):       
        
        self.parser.add_argument('-q','--query', 
                                            required=True
                                            )

        self.parser.add_argument('-cf','--checkform', 
                                            action="store_true", 
                                                required=False
                                                )

        self.parser.add_argument('-n','--number' ,
                                                required=False, default=5
                                                )

        self.parser.add_argument('-t','--timeout', 
                                                required=False, default=2.0
                                                )


        args = self.parser.parse_args()   

        return args

