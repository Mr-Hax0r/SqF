from requests import exceptions, get


class Vunls():
    def __init__(self, timeout):
        self.payloads = ["'", "\"", "\\", "/"]
        self.timeout = timeout

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

        for payload in self.payloads:
            try:
                response = get(url+payload, timeout=self.timeout)
                if self._check_error(response):
                    return True
                else:
                    pass   

            except exceptions.HTTPError:
                continue
            except exceptions.ConnectionError:
                continue
            except exceptions.ReadTimeout:
                continue
            except exceptions.MissingSchema:   
                continue
            except exceptions.TooManyRedirects:
                continue
        return False    


