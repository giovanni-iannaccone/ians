from getpass import getpass
from rich.console import Console

import os
import socket
import sys
import threading

def ascii_art():
    banner = """

                                         |
                                         |
                                         |
                                         |
   _______                   ________    |
  |ooooooo|      ____       | __  __ |   |
  |[]+++[]|     [____]      |/  \/  \|   |
  |+ ___ +|     ]()()[      |\__/\__/|   |
  |:|   |:|   ___\__/___    |[][][][]|   |
  |:|___|:|  |__|    |__|   |++++++++|   |
  |[]===[]|   |_|_/\_|_|    | ______ |   |
_ ||||||||| _ | | __ | | __ ||______|| __|
  |_______|   |_|[::]|_|    |________|   \.
              \_|_||_|_/                  \.
                |_||_|                     \.
               _|_||_|_                     \.
      ____    |___||___|                     \.
     /  __\          ____                     \.
     \( oo          (___ \                     \.
     _\_o/           oo~)/
    / \|/ \         _\-_/_
   / / __\ \___    / \|/  \.
   \ \|   |__/_)  / / .- \ \.
    \/_)  |       \ \ .  /_/
     ||___|        \/___(_/
     | | |          | |  |
     | | |          | |  |
     |_|_|          |_|__|
     [__)_)        (_(___]

    """

    console.print(banner, style="bold")

def block(nickname):
    addr = address[nicknames.index(nickname)]
    blocked_users.append(addr[0])
    remove_blocked(addr)
    print(blocked_users)

def broadcast(message):
    for client in clients:
        client.send(message)

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def exiting():
    message = "[-] The room gets closed by the host".encode()
    console.print("[-] Closing chat ...", style="bold red")
    console.print("Remember, always use ssh", style="bold red")
    try:
        for client in clients:
            client.send(message)
            remove(nicknames[clients.index(client)])
    except NameError:
        pass
    sys.exit()

def handle(client):
    while True:
        try:
            message = client.recv(8192)
            if client in clients:
                broadcast(message)
        except:
            try:
                index = clients.index(client)
                nickname = nicknames[index]
                remove(nickname)
                broadcast("{} left!".format(nickname).encode())
            except ValueError:
                pass

def initialize():
    try:
        global address, blocked_users, clients, console, nicknames, password, server
        console = Console()
        ascii_art()
        
        console.print("    A simple ssh chat room's server", style="bold red")
        host = console.input("\n[bold blue][+][/bold blue] Type here the ip you want to use: ")

        while True:
            try:        
                port = int(console.input("[bold blue][+][/bold blue] Type the port: "))
            except:
                console.print("Invalid input", style="italica yellow")
                port = int(console.input("[bold blue][+][/bold blue] Type the port: "))
            else:
                break

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen()

        address = []
        blocked_users = []
        clients = []
        nicknames = []
        password = getpass()
        console.print("[+] Server is listening ...", style="bold blue")
        receive()

    except KeyboardInterrupt:
        exiting()

def receive():
    while True:
        client, addr = server.accept()
        address.append(addr)
        clients.append(client)

        if addr[0] in blocked_users:
            remove_blocked(addr)
            continue

        while client.recv(2048).decode() != password:
            client.send("[-] Wrong password".encode())
            
        client.send("True".encode())

        console.print("[bold blue][+][/bold blue] Connected with [bold blue]{}[/bold blue]".format(str(addr)))

        client.send("NICK".encode())
        nickname = client.recv(1024).decode()
        nicknames.append(nickname)

        console.print("[bold blue][+][/bold blue] Nickname is {}".format(nickname))
        broadcast("[+] {} joined!".format(nickname).encode())
        client.send("[+] Connected to server!".encode())

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

        write_thread = threading.Thread(target=write)
        write_thread.start()

def remove(connection):
    index = nicknames.index(connection)
    clients[index].close()
    clients.pop(index)
    address.pop(index)
    nicknames.remove(connection)

def remove_blocked(connection):
    index = address.index(connection)
    address.remove(connection)

    clients[index].close()
    clients.pop(index)

def show_info(nickname):
    try:
        ip, port = address[nicknames.index(nickname)]
        console.print(f"[bold blue][+][/bold blue] Ip: [bold green]{ip}[/bold green]")
        console.print(f"[bold blue][+][/bold blue] Port: [bold green]{port}[/bold green]")
        console.print(f"[bold blue][+][/bold blue] Nickname: [bold green]{nickname}[/bold green]")
    except ValueError:
        console.print(f"{nickname} not in this room", style="bold red")

def write():
    while True:
        cmd = input("> ")
        cmd = list(cmd.split())
        if cmd[0] in  ("-h", "--help"):
            console.print("[+] Servers's host has special 'powers', type:", style="bold blue")
            console.print("\t-[bold blue]block 'nickname'[/bold blue] \tto don't allow him to enter to this session")
            console.print("\t-[bold blue]clear[/bold blue] \t\t\tto clear the screen")
            console.print("\t-[bold blue]exit[/bold blue] \t\t\tto close the room for everybody")
            console.print("\t-[bold blue]info 'nickname'[/bold blue] \tto have information on a nickname (his ip & port )")
            console.print("\t-[bold blue]ls[/bold blue] \t\t\tto show all connected user")
            console.print("\t-[bold blue]remove 'nickname'[/bold blue] \tto remove an user")

        elif cmd[0] == "block":
            block(cmd[1])
            print(f"Blocked users: {blocked_users}")
            
        elif cmd[0] == "clear":
            clear_screen()

        elif cmd[0] == "exit":
            exiting()

        elif cmd[0] == "info":
            show_info(cmd[1]) 

        elif cmd[0] == "ls":
            console.print(f"[bold blue][+][/bold blue] Connected: [bold green]{[nickname for nickname in nicknames]}[/bold green]")
            console.print(f"[bold blue][+][/bold blue] Connected: [bold green]{[addr[0] for addr in address]}[/bold green]")

        elif cmd[0] == "remove":
            remove(cmd[1])
    
        else:
            console.print("[-] Invalid syntax, type -h or --help for more informations", style="bold red")