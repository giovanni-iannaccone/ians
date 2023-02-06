from rich.console import Console

import os
import queue
import requests
import sys
import threading

def dir_bruter(words):
    headers = {"User-Agent": AGENT}
    while not words.empty():
        url = f"{TARGET}{words.get()}"

        try:
            r = requests.get(url, headers=headers)
        except requests.exceptions.ConnectionError:
            console.print(f"{url} not found\t\t", end="\r", style="red")
            continue

        if r.status_code == 200:
            console.print(f"\nSuccess {url} : {r.status_code}", style="bold blue")

        else:
            print(f"{url} => {r.status_code}")
        
        directory.append(f"{url} : {r.status_code}")

        try:
            with open(f"{TARGET}.txt", "w") as f:
                f.write(directory)
        except Exception as e:
            print(f"{e}: creating file {TARGET}.txt")
            os.system(f"touch {TARGET}.txt")

    exiting()

def exiting():
    console.print("\n\nFound: ", style="bold blue")
    if directory ==  []:
        console.print("No directory were found", style="bold red")

    else:
        for i in directory:
            console.print(i, style="bold green")
        
    console.print("Exiting...", style="bold red")
    sys.exit()

def get_words(resume=None):

    def extend_words(word):
        if "." in word:
            words.put(f"/{word}")
        else:
            words.put(f"/{word}/")
        
        for extension in EXTENSIONS:
            words.put(f"/{word}{extension}")

    while True:
        try:
            with open(WORDLIST) as f:
                raw_words = f.read()
        except Exception:
            WORDLIST = "./utils/little_dictionary.txt"
        else:
            break


    found_resume = False
    words = queue.Queue()
    for word in raw_words.split():
        if resume is not None:
            if found_resume:
                extend_words(word)
            elif word == resume:
                found_resume == True
                console.print(f"Resuming wordlist from [bold blue]{resume}[/bold blue]")
        else:
            extend_words(word)

    return words
        
def initialize():
    global console, directory, AGENT, EXTENSIONS, TARGET, THREADS, WORDLIST
    console = Console()
    directory = []

    show_banner()
    console.print("\t\tA site directories's bruteforce tool\n", style="bold red")
    AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0 "

    EXTENSIONS = [".bak", ".html", ".inc", ".js", ".orig", ".php"]
    try:

        TARGET = console.input("[bold blue][+][/bold blue] Type the target: ")
        THREADS = os.cpu_count()
        console.print("\nYou can use our ./utils/little_dictionary.txt", style="red")
        WORDLIST = console.input("[bold blue][+][/bold blue] Enter the directory where you have the wordlist: ")
        words = get_words()
        console.print(f"[bold blue][+][/bold blue] The found directories/files will be saved on {TARGET}.txt")
        console.print("\nPress [bold blue]ENTER[/bold blue] to continue")
        sys.stdin.readline()
        
        for _ in range(THREADS):
            t = threading.Thread(target=dir_bruter, args=(words,))
            t.start()
        
        while True:
            pass

    except KeyboardInterrupt:
        exiting()

def show_banner():
    banner =  """
    
                                ______
                             .-"      "-.
                            /            \.
                           |              |
                           |,  .-.  .-.  ,|
                           | )(__/  \__)( |
                           |/     /\     \|
      (@_                  (_     ^^     _)
 _     ) \__________________\__|IIIIII|__/_________________________
(_)@8@8{}<___________________|-\IIIIII/-|__________________________>
       )_/                   \          /
      (@                      `--------` 

    """
    console.print(banner, style="bold blue")
