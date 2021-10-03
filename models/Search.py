from random import choice
from colorama import Fore
from colorama.initialise import init
from googlesearch import  search
import googlesearch

init()

class Search():
    def __init__(self, query, number, timeout):
        self.query = query
        self.number = number
        self.timeout = timeout
        self.results = []

    def _load_user_agent_random(self):
        with open("lists/user_agents.txt", "r") as user_agent:
            user_agents = user_agent.read().splitlines()
            user_agent = choice(list(user_agents))

        return user_agent


    def _load_tld_google_random(self):
        with open("lists/google_url.txt", "r") as google_url:
            google_tlds = google_url.read().splitlines()
            google_tld = choice(list(google_tlds))

        return google_tld


    def _load_blacklist(self):
        with open('lists/blacklist.txt') as links:
            lines = links.read().splitlines()

        return lines

    def _check_url(self):
        blacklist = self._load_blacklist()
        for r in self.results:
            if any(b in r for b in blacklist):
                self.results.remove(r)

        return self.results        
                
    def search(self):
        google_tld = self._load_tld_google_random()
        user_agent = self._load_user_agent_random()

        print(Fore.GREEN +  f"Random google URL: https://google.{google_tld}/search/")
        print(Fore.GREEN +  f"Random User-Agent: {user_agent}")
        
        for target in search(self.query, tld=google_tld, 
                            num=5, 
                                stop=self.number, 
                                    pause=self.timeout, user_agent=user_agent):
                     
            self.results.append(target)
            #self._check_url()
        if self.results == []:
            print(f'\n[+] {len(self.results)} results found. Google may block you and '+ Fore.RED +'try again.')
            exit(0)
        return self.results   

