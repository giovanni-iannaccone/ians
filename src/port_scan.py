from multiprocessing.pool import ThreadPool
from rich.console import Console
from rich.table import Table

import json
import os
import socket
import sys

def display_progress(loop_index, iterable_length):
    bar_max_width = 38
    bar_width = bar_max_width * loop_index // iterable_length
    bar = ("▉" * bar_width)  + ("-" * (bar_max_width - bar_width))
    progress = "%.1f"%(loop_index / iterable_length * 100)
    progress = progress if progress != "99.9" else "100"
    bar = bar if progress != "100" else bar.replace("-", "▉")
    console.print(f"[{bar}] {progress} %\t\t", end="\r", style="bold blue")
    if loop_index == iterable_length:
        print("\n\n")

def exiting():
    console.print("\nExiting ...", style="bold red")
    sys.exit()

def extract_json():
    with open("./utils/common_ports.json", "r") as file:
        data = json.load(file)
        file.close()
        return data

def threadpool_executer(function, iterable, iterable_length):
    n_of_workers = os.cpu_count()
    loop_index = 0
    try:
        console.print(f"{n_of_workers} core will be used\n", style="bold green")
        with ThreadPool(n_of_workers) as pool:
            for loop_index, _ in enumerate(pool.imap(function, iterable)):
                display_progress(loop_index, iterable_length)
    except KeyboardInterrupt:
        return 

class Scanner:
    def __init__(self):
        self.open_ports = []
        self.ports_info = {}
        self.remote_host = ""

    def get_ports_info(self):
        data =  extract_json()
        self.ports_info = {int(k): v for (k, v) in data.items()}
 
    def get_host_ip_addr(self, target):
        try:
            ip_addr = socket.gethostbyname(target)
        except socket.gaierror as e:
            print(f"An error occured: {e}")
        else:
            return ip_addr

    def initialize(self):
        global console, option
        console = Console()
        show_banner()
        console.print("\n     A multithread port scanner\n", style="bold red")
        try:
            target = console.input("[bold blue][+][/bold blue] Type the target: ")
        except KeyboardInterrupt:
            exiting()

        self.remote_host = self.get_host_ip_addr(target)
        try:
            ip_addr = socket.gethostbyname(target)
        except socket.gaierror as e:
            print(f"An error occurred: {e}")
        else:
            try:
                console.print(f"IP address for [bold red]{target}[/bold red] acquired: [bold blue]{ip_addr}[bold blue]")
                self.get_ports_info()

                option = int(console.input("\n[bold blue][1][/bold blue] for a base scan\n[bold blue][2][/bold blue] for a complete scan\nType> "))
                while option not in (1, 2):
                    console.print("Invalid option", style="italic yellow")
                    option = int(console.input("\n[bold blue][1][/bold blue] for a base scan\n[bold blue][2][/bold blue] for a complete scan\nType> "))

                if option == 1:
                    ports = self.ports_info.keys()
                else:
                    ports = []
                    for i in range(1, 65536):
                        ports.append(i)

                console.input("[red]\nScanner is ready, press [bold]ENTER[/bold] to start...[/red] ")
            except KeyboardInterrupt:
                exiting()
            else:
                self.run(ports)

    def run(self, ports):
        print("\n")
        threadpool_executer(self.scan_port, ports, 65535 if option == 2 else len(ports))
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("PORT", style="blue")
        table.add_column("STATE", style="blue", justify="center")
        table.add_column("SERVICE", style="blue")

        print("\n\n")
        if self.open_ports:
            for port in self.open_ports:
                table.add_row(str(port), "OPEN", self.safe_excecuter(port))
            console.print(table)
            console.print(f"\nThere are [bold blue]{len(self.open_ports)}[/bold blue] open ports")
        else:
            console.print("There are 0 open ports (O_O；)", style="bold red")
        exiting()

    def safe_excecuter(self, port):
        try:
            return self.ports_info[port]
        except Exception:
            return "?"
            
    def scan_port(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.0)
        conn_status = sock.connect_ex((self.remote_host, port))
        if conn_status == 0:
            self.open_ports.append(port)
        sock.close()
    
def show_banner():
    banner = """
     ___
   ,'._,`.
  (-.___.-)
  (-.___.-)
  `-.___.-'                  
   ((  @ @|              .            __
    \   ` |         ,\   |`.    @|   |  |      _.-._
   __`.`=-=mm===mm:: |   | |`.   |   |  |    ,'=` '=`.
  (    `-'|:/  /:/  `/  @| | |   |, @| @|   /---)W(---\.
   \ \   / /  / /         @| |   '         (----| |----) ,~
   |\ \ / /| / /            @|              \---| |---/  |
   | \ V /||/ /                              `.-| |-,'   |
   |  `-' |V /                                 \| |/    @'
   |    , |-'                                 __| |__
   |    .;: _,-.                         ,--""..| |..""--.
   ;;:::' "    )                        (`--::__|_|__::--')
 ,-"      _,  /                          \`--...___...--'/   
(    -:--'/  /                           /`--...___...--'\.
 "-._  `"'._/                           /`---...___...---'\.
     "-._   "---.                      (`---....___....---')
      .' ",._ ,' )                     |`---....___....---'|
      /`._|  `|  |                     (`---....___....---') 
     (   \    |  /                      \`---...___...---'/
      `.  `,  ^""                        `:--...___...--;'
        `.,'                               `-._______.-'
                             
            """

    console.print(banner, style="bold blue")
