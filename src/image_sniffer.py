from rich.console import Console
from scapy.all import IP, sniff, TCP

import sys

def exiting():
    console.print("Exiting...", style="bold red")
    sys.exit()

def initialize():
    try:
        global console
        console = Console()
        show_banner()
        console.print("\n\tAn email credential sniffer", style="bold red")
        ports = "tcp port 80"
        console.print(f"\n     Waiting for an information from: \n\t       [bold green]{ports}[/bold green]")
        sniff(filter=ports, prn=image_searcher, store=0)
    except KeyboardInterrupt:
        exiting()

def image_searcher(packet):
    if packet[TCP].payload:
        mypacket = str(packet[TCP].payload)
        if mypacket.upper().endswith(".JPG") or mypacket.upper().endswith(".PNG"):
            console.print(f"[bold blue][+][/bold blue] Destination: {packet[IP].dst}")
            console.print(packet[TCP].payload, style="bold blue")

def show_banner():
    banner = """
                                       /|
                                     |\|
                                     |||
                                     |||
                                     |||
                                     |||
                                     |||
                                     |||
                                  ~-[{=}]-~
                                     |/|
                                     |/|
             ///~`     |\._          `0'         =\-\.         . .
            ,  |='  ,))\_| ~-_                    _)  \      _/_/|
           / ,' ,;((((((    ~ \                  `~~~\-~-_ /~ (_/\.
         /' -~/~)))))))'\_   _/'                      \_  /'  D   |
        (       (((((( ~-/ ~-/                          ~-;  /    \--_
         ~~--|   ))''    ')  `                            `~~\_    \   )
             :        (_  ~\           ,                    /~~-     ./
              \        \_   )--__  /(_/)                   |    )    )|
    ___       |_     \__/~-__    ~~   ,'      /,_;,   __--(   _/      |
  //~~\`\    /' ~~~----|     ~~~~~~~~'        \-  ((~~    __-~        |
((()   `\`\_(_     _-~~-\                      ``~~ ~~~~~~   \_      /
 )))     ~----'   /      \                                   )       )
  (         ;`~--'        :                                _-    ,;;(
            |    `\       |                             _-~    ,;;;;)
            |    /'`\     ;                          _-~          _/
           /~   /    |    )                         /;;;''  ,;;:-~
          |    /     / | /                         |;;'   ,''
          /   /     |  \.|                         |   ,;(    
        _/  /'       \  \_)                   .---__\_    \,--._______
       ( )|'         (~-_|                   (;;'  ;;;~~~/' `;;|  `;;;\.
        ) `\_         |-_;;--__               ~~~----__/'    /'_______/
        `----'       (   `~--_ ~~~;;------------~~~~~ ;;;'_/'
                     `~~~~~~~~'~~~-----....___;;;____---~~
    
    """

    console.print(banner, style="bold red")