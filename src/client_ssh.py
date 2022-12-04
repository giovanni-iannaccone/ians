from datetime import datetime
from getpass import getpass
from rich.console import Console

import socket
import sys
import threading

def ascii_art():
    banner = """
                                      .
     .              .   .'.     \   /
   \   /      .'. .' '.'   '  -=  o  =-
 -=  o  =-  .'   '              / | \.
   / | \                          |
     |                            |
     |                            |
     |                      .=====|
     |=====.                |.---.|
     |.---.|                ||=o=||
     ||=o=||                ||   ||
     ||   ||                ||   ||
     ||   ||                ||___||
     ||___||                |[:::]|
     |[:::]|                '-----'
     '-----'
    
    """
    console.print(banner, style="bold")

def initialize():
    global console, client, nickname
    console = Console()
    
    ascii_art()
    console.print("   A simple ssh chat room's client", style="bold red")

    nickname = console.input("\n[bold blue][+][/bold blue] Choose a nickname: ")
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    ip = str(console.input("[bold blue][+][/bold blue] Type the ip of the room's server: "))
    port = int(console.input("[bold blue][+][/bold blue] Type the port of the room's server: "))

    try:
        client.connect((ip, port))
    except ConnectionAbortedError:
        console.print("[-] You probably are blocked in this session", style="bold red")
        sys.exit()

    while True:
        acceptation = None
        password = getpass()
        client.send(password.encode())
        acceptation = client.recv(2048).decode()
        if acceptation == "True":
            break
        else:
            console.print(acceptation, style="bold red")

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()

    while True:
        pass

def receive():
    while True:
        try:
            message = client.recv(8192).decode()
            if message == "NICK":
                client.send(nickname.encode())

            elif message == "[-] The room gets closed by the host":
                console.print(message, style="bold red")
                client.close()

            else:
                console.print(f"[green]{message}[/green]" + "\t\t\t" + str(datetime.now()))
        except:
            continue

def write():
    while True:
        try:
            message = f"{nickname}: {input('')}"
            client.send(message.encode())
        except KeyboardInterrupt:
            print("[-] Closing chat ...")
            client.close()
        except OSError:
            sys.exit()