from rich.console import Console

import contextlib
import os
import queue
import requests
import sys
import threading
import time 

def gather_paths():
    for root, _, files in os.walk("."):
        for fname in files:
            if os.path.splitext(fname)[1] in FILTERED:
                continue
            path = os.path.join(root, fname)
            if path.startswith("."):
                path = path[1:]
            print(path)
            web_paths.put(path)

@contextlib.contextmanager
def chdir(path):
    this_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(this_dir)
    
def test_remote():
    while not web_paths.empty:
        path = web_paths.get()
        url = f"{TARGET}{path}"
        time.sleep(2)
        r = requests.get(url)
        if r.status_code == 200:
            answers.put(url)
        else:
            sys.stdout.write("x")
        sys.stdou.flush()

def run():
    mythreads = list()
    for i in range(THREADS):
        console.print(f"Spawning thread [bold blue]{i}[/bold blue]")
        t = threading.Thread(target=test_remote)
        mythreads.append(t)
        t.start()
    
    for thread in mythreads:
        thread.join()

def initialize():
    global console, FILTERED, TARGET, THREADS, answers, web_paths
    console = Console()

    show_banner()
    console.print("\n\t\t\t\t   A site mapper\n", style="bold red")
    FILTERED = [".jpg", ".png", ".gif", ".css"]
    TARGET = console.input("[bold blue][+][/bold blue] Type the target: ")
    THREADS = os.cpu_count()

    answers = queue.Queue()
    web_paths = queue.Queue()

    with chdir(console.input("[bold blue][+][/bold blue] Enter the directory of the copy of the site: ")):
        gather_paths()
        
    console.input("Presso [bold blue]ENTER[/bold blue] to continue...")
    with open("myanswer.txt", "w") as f:
        while not answers.empty():
            f.write(f"{answers.get()}\n")
    print("Done")

def show_banner():
    banner = """
    $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'               `$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$  
    $$$$$$$$$$$$$$$$$$$$$$$$$$$$'                   `$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    $$$'`$$$$$$$$$$$$$'`$$$$$$!                       !$$$$$$'`$$$$$$$$$$$$$'`$$$
    $$$$  $$$$$$$$$$$  $$$$$$$                         $$$$$$$  $$$$$$$$$$$  $$$$
    $$$$. `$' \' \$`  $$$$$$$!                         !$$$$$$$  '$/ `/ `$'  .$$$$
    $$$$$. !\  i  i .$$$$$$$$                           $$$$$$$$. i  i  /! .$$$$$
    $$$$$$   `--`--.$$$$$$$$$                           $$$$$$$$$.--'--'   $$$$$$
    $$$$$$L        `$$$$$^^$$                           $$^^$$$$$'        J$$$$$$
    $$$$$$$.   .'   ""~   $$$    $.                 .$  $$$   ~""   `.   .$$$$$$$
    $$$$$$$$.  ;      .e$$$$$!    $$.             .$$  !$$$$$e,      ;  .$$$$$$$$
    $$$$$$$$$   `.$$$$$$$$$$$$     $$$.         .$$$   $$$$$$$$$$$$.'   $$$$$$$$$
    $$$$$$$$    .$$$$$$$$$$$$$!     $$`$$$$$$$$'$$    !$$$$$$$$$$$$$.    $$$$$$$$
    $$$$$$$     $$$$$$$$$$$$$$$$.    $    $$    $   .$$$$$$$$$$$$$$$$     $$$$$$$
                                    $    $$    $
                                    $.   $$   .$
                                    `$        $'
                                     `$$$$$$$$'

    """

    console.print(banner, style="bold green")