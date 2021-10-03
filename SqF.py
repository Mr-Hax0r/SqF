from http.client import SEE_OTHER
import time
from models.Search import Search
from time import gmtime, strftime
from models.Vuln import Vunls
from models.Forms import VunlForms
from models.Argparser import Args
from time import sleep
from urllib.parse import urlparse
from colorama import Fore
from colorama.initialise import init
from os import name, system

def clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')


init()
def banner():
    banner = '''
███████╗ ██████╗ ███████╗
██╔════╝██╔═══██╗██╔════╝
███████╗██║   ██║█████╗  
╚════██║██║▄▄ ██║██╔══╝  
███████║╚██████╔╝██║     
╚══════╝ ╚══▀▀═╝ ╚═╝     
        SQL injection scanner By [ Mr Hax0r ]
        Github :  https://github.com/Mr-Hax0r/SqF.git
        Telegram : @Mr_hax0r\n\n
    '''
    print(banner)


def app():
    args = Args().argparser()
    results = Search(
        query=args.query, number=int(args.number), timeout=int(bool(args.timeout))).search()
    v = Vunls(timeout=int(bool(args.timeout)))
    try:
        print(Fore.WHITE +  f'\n[+] Scanning. Press Ctrl+C To Exit.  {Fore.GREEN}[{strftime("%H:%M:%S", gmtime())}]\n\n') 
        print(f'{Fore.GREEN}[{strftime("%H:%M:%S", gmtime())}] {Fore.CYAN}[ INFO ] {Fore.WHITE}Found {len(results)} url to check .. \n')       
        vulnerable = []
        for item in results:
            is_vull = 'vulnerable' if v.check_vull(item)  else ''
            print(f'{Fore.GREEN}[{strftime("%H:%M:%S", gmtime())}] {Fore.CYAN}[ Scanning ] {Fore.WHITE}{item}  {Fore.GREEN}{is_vull}')   
    except KeyboardInterrupt:
        exit(0)   
    if args.checkform:
        print(Fore.WHITE +  f'\nChecking Forms. Press Ctrl+C To Exit.  {Fore.GREEN}[{strftime("%H:%M:%S", gmtime())}]\n\n')
        form_check = VunlForms(timeout=int(bool(args.timeout)))
        for item in results:
            form_check.check_vull(item)

                    


if __name__ == '__main__':
    clear()
    banner()
    app()






