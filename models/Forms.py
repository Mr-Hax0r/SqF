from bs4 import BeautifulSoup as bs
from colorama import Fore
from colorama.initialise import init
from random import choice
from time import gmtime, strftime
from googlesearch import search
from requests import Session
from urllib.parse import urljoin
init()



class VunlForms():
    def __init__(self, timeout):
        self.payloads = ["'", "\"", "\\", "/"]
        self.timeout = timeout
        self.s = Session()
        self.s.headers["User-Agent"] = self._load_user_agent_random()


    def _load_user_agent_random(self):
        with open("lists/user_agents.txt", "r") as user_agent:
            user_agents = user_agent.read().splitlines()
            user_agent = choice(list(user_agents))

        return user_agent


    def get_all_forms(self, url):
        soup = bs(self.s.get(url, timeout=self.timeout).content, "html.parser")
        return soup.find_all("form")

    def get_form_details(self, form):
        details = {}
        try:
            action = form.attrs.get("action").lower()
        except:
            action = None
        method = form.attrs.get("method", "get").lower()
        inputs = []
        for input_tag in form.find_all("input"):
            input_type = input_tag.attrs.get("type", "text")
            input_name = input_tag.attrs.get("name")
            input_value = input_tag.attrs.get("value", "")
            inputs.append({"type": input_type, "name": input_name, "value": input_value})
        details["action"] = action
        details["method"] = method
        details["inputs"] = inputs
        return details

    def _check_error(self, response):
        try:
            errors = {
                # MySQL
                "you have an error in your sql syntax;",
                "warning: mysql",
                # SQL Server
                "unclosed quotation mark after the character string",
                # Oracle
                "quoted string not properly terminated",
            }
            for error in errors:
                if error in response.content.decode().lower():
                    return True
            return False    
        except:
            pass    

    def check_vull(self, url):
        try:
            forms = self.get_all_forms(url)
            if len(forms) > 0:
                print(f'{Fore.GREEN}[{strftime("%H:%M:%S", gmtime())}] {Fore.YELLOW}[ Detecte ] {Fore.WHITE}Detected {len(forms)} forms on {url}')
            else:
                print(f'{Fore.GREEN}[{strftime("%H:%M:%S", gmtime())}] {Fore.YELLOW}[ Detecte ] {Fore.WHITE}Detected {len(forms)} forms on {url}')   
            for form in forms:
                form_details = self.get_form_details(form)  
                for payload in self.payloads:
                    data = {}
                    for input_tag in form_details["inputs"]:
                        if input_tag["type"] == "hidden" or input_tag["value"]:
                            try:
                                data[input_tag["name"]] = input_tag["value"] + payload
                            except:
                                pass
                        elif input_tag["type"] != "submit":
                            data[input_tag["name"]] = f"test{payload}"
                    url = urljoin(url, form_details["action"])
                    if form_details["method"] == "post":
                        response = self.s.post(url, data=data)
                    elif form_details["method"] == "get":
                        response = self.s.get(url, params=data)
                    if self._check_error(response):
                        print(f'{Fore.GREEN}[{strftime("%H:%M:%S", gmtime())}] {Fore.GREEN}[ INFO ] {Fore.WHITE}SQL Injection vulnerability detected, link: {url}')
                        break
        except KeyboardInterrupt:
            exit(0)            


