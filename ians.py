from rich.console import Console

import src.arper as arper
import src.bruteforce as bruteforce
import src.client_ssh as client_ssh
import src.directory_bruter as directory_bruter
import src.ddos as ddos
import src.image_sniffer as image_sniffer
import src.mail_sniffer as mail_sniffer
import src.mapper as mapper
import src.port_scan as port_scan
import src.server_ssh as server_ssh
import src.sniffer as sniffer
import src.trojan_creation as trojan_creation
import src.user_finder as user_finder

import os
import subprocess
import sys
import time

def arp_a():
    clear_screen()
    output = subprocess.check_output("arp -a", shell=True)

    if os.name == "nt":
        console.print(output, style="bold blue")
    else:
        output = output.decode()
        print("Connected:\n")
        users = 0

        for line in output.split():
            if "." in line:
                console.print(f"IP: [bold blue]{line}[/bold blue]")
                users += 1
            elif ":" in line or line == "<incomplete>":
                console.print(f"MAC: [bold blue]{line}[/bold blue]") 
            elif line not in ("?", "at", "[ether]", "on"):
                console.print(f"Interface: [bold blue]{line}[/bold blue]")
                print()
            

        console.print(f"\n\n{users} users connected", style="green")
    console.input("[red]Press [bold]ENTER[/bold] to return to the menu...[red]")
    main()

def ascii_art_ians():
    clear_screen()
    banner = f""" 
                          ╔══════════════ Giovanni Iannaccone ═══════════════╗
                          ║                                                  ║
                          ║        /$$$$$$  /$$$$$$  /$$   /$$  /$$$$$$      ║
                   / V\   ║       |_  $$_/ /$$__  $$| $$$ | $$ /$$__  $$     ║
                 / `  /   ║         | $$  | $$  \ $$| $$$$| $$| $$  \__/     ║
                <<   |    ║         | $$  | $$$$$$$$| $$ $$ $$|  $$$$$$      ║
                /    |    ║         | $$  | $$__  $$| $$  $$$$ \____  $$     ║
              /      |    ║         | $$  | $$  | $$| $$\  $$$ /$$  \ $$     ║
            /        |    ║        /$$$$$$| $$  | $$| $$ \  $$|  $$$$$$/     ║
           /    \  \ /    ║       |______/|__/  |__/|__/  \__/ \______/      ║
          (      ) | |    ║                                                  ║
 ________ |   _/_  | |    ║      ︻┻┳══━一   ~ Version {version} ~    ︻┻┳══━一    ║          
<__________\______)\__)   ╚══════════════════════════════════════════════════╝

                """
    console.print(banner, style="bold green")

    console.print("\n    FOR EDUCATIONAL PURPOSE ONLY", style="bold red")
    console.print("\n    SELECT AN OPTION TO CONTINUE", style="bold")
    
def ascii_art_warning():
    console.print("═" * 121, style="bold red")
    console.print("═" * 38 + " https://github.com/giovanni-iannaccone/ians " + "═" * 38, style="bold red")
    console.print("═" * 121, style="bold red")

    banner = """ 


  █████▒▒█████   ██▀███     ▓█████ ▓█████▄  █    ██  ▄████▄   ▄▄▄     ▄▄▄█████▓ ██▓ ▒█████   ███▄    █  ▄▄▄       ██▓       
▓██   ▒▒██▒  ██▒▓██ ▒ ██▒   ▓█   ▀ ▒██▀ ██▌ ██  ▓██▒▒██▀ ▀█  ▒████▄   ▓  ██▒ ▓▒▓██▒▒██▒  ██▒ ██ ▀█   █ ▒████▄    ▓██▒       
▒████ ░▒██░  ██▒▓██ ░▄█ ▒   ▒███   ░██   █▌▓██  ▒██░▒▓█    ▄ ▒██  ▀█▄ ▒ ▓██░ ▒░▒██▒▒██░  ██▒▓██  ▀█ ██▒▒██  ▀█▄  ▒██░       
░▓█▒  ░▒██   ██░▒██▀▀█▄     ▒▓█  ▄ ░▓█▄   ▌▓▓█  ░██░▒▓▓▄ ▄██▒░██▄▄▄▄██░ ▓██▓ ░ ░██░▒██   ██░▓██▒  ▐▌██▒░██▄▄▄▄██ ▒██░       
░▒█░   ░████▓▒░░██▓ ▒██▒   ░▒████▒░▒████▓ ▒▒█████▓ ▒ ▓███▀ ░ ▓█   ▓██▒ ▒██▒ ░ ░██░░ ████▓▒░▒██░   ▓██░ ▓█   ▓██▒░██████▒
 ▒ ░   ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░   ░░ ▒░ ░ ▒▒▓  ▒ ░▒▓▒ ▒ ▒ ░ ░▒ ▒  ░ ▒▒   ▓▒█░ ▒ ░░   ░▓  ░ ▒░▒░▒░ ░ ▒░   ▒ ▒  ▒▒   ▓▒█░░ ▒░▓  ░
 ░       ░ ▒ ▒░   ░▒ ░ ▒░    ░ ░  ░ ░ ▒  ▒ ░░▒░ ░ ░   ░  ▒     ▒   ▒▒ ░   ░     ▒ ░  ░ ▒ ▒░ ░ ░░   ░ ▒░  ▒   ▒▒ ░░ ░ ▒  ░
 ░ ░   ░ ░ ░ ▒    ░░   ░       ░    ░ ░  ░  ░░░ ░ ░ ░          ░   ▒    ░       ▒ ░░ ░ ░ ▒     ░   ░ ░   ░   ▒     ░ ░
           ░ ░     ░           ░  ░   ░       ░     ░ ░            ░  ░         ░      ░ ░           ░       ░  ░    ░  ░
                                    ░               ░                                                                            
 ██▓███   █    ██  ██▀███   ██▓███   ▒█████    ██████ ▓█████     ▒█████   ███▄    █  ██▓   ▓██   ██▓                               
▓██░  ██▒ ██  ▓██▒▓██ ▒ ██▒▓██░  ██▒▒██▒  ██▒▒██    ▒ ▓█   ▀    ▒██▒  ██▒ ██ ▀█   █ ▓██▒    ▒██  █                                
▓██░ ██▓▒▓██  ▒██░▓██ ░▄█ ▒▓██░ ██▓▒▒██░  ██▒░ ▓██▄   ▒███      ▒██░  ██▒▓██  ▀█ ██▒▒██░     ▒██ ██░                             
▒██▄█▓▒ ▒▓▓█  ░██░▒██▀▀█▄  ▒██▄█▓▒ ▒▒██   ██░  ▒   ██▒▒▓█  ▄    ▒██   ██░▓██▒  ▐▌██▒▒██░     ░ ▐██▓░                             
▒██▒ ░  ░▒▒█████▓ ░██▓ ▒██▒▒██▒ ░  ░░ ████▓▒░▒██████▒▒░▒████▒   ░ ████▓▒░▒██░   ▓██░░██████▒ ░ ██▒▓░                            
▒▓▒░ ░  ░░▒▓▒ ▒ ▒ ░ ▒▓ ░▒▓░▒▓▒░ ░  ░░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░░░ ▒░ ░   ░ ▒░▒░▒░ ░ ▒░   ▒ ▒ ░ ▒░▓  ░  ██▒▒▒
░▒ ░     ░░▒░ ░ ░   ░▒ ░ ▒░░▒ ░       ░ ▒ ▒░ ░ ░▒  ░ ░ ░ ░  ░     ░ ▒ ▒░ ░ ░░   ░ ▒░░ ░ ▒  ░▓██ ░▒░                            
░░        ░░░ ░ ░   ░░   ░ ░░       ░ ░ ░ ▒  ░  ░  ░     ░      ░ ░ ░ ▒     ░   ░ ░   ░ ░   ▒ ▒ ░░                          
            ░        ░                  ░ ░        ░     ░  ░       ░ ░           ░     ░  ░░ ░
                                                                                            ░ ░

"""
    
    console.print(banner, style="bold red")

    console.print("═" * 121, style="bold red")
    console.print("═ WARNING ═" * 11, style="bold red")
    console.print("═" * 121, style="bold red")

    console.print("\n\t\t\tThe author is not responsible for any malicious use of this tool", style="bold red")
    console.input("\n[red]Press [bold]ENTER[/bold] to continue[/red] ")

def chat_option():
    console.print("[bold blue][1][/bold blue] if you want to host the server")
    console.print("[bold blue][2][/bold blue] if you want to connect to a server")
    console.print("[bold blue][3][/bold blue] to return to the menu")

    option = int(console.input("\n┌── [[bold green]$ IANS $[/bold green]] ── [[bold red]chat[/bold red]]:\n└───> "))
    while option not in (1, 2, 3):
        console.print("Invalid choice", style="italic yellow")
        option = int(console.input("\n┌── [[bold green]$ IANS $[/bold green]] ── [[bold red]chat[/bold red]]:\n└───> "))
    
    clear_screen()
    if option == 1:
        server_ssh.initialize()
    elif option == 2:
        client_ssh.initialize()
    else:
        main()

def clear_screen():
    os.system("cls" if os == "nt" else "clear")

def exiting():
    console.print("\n[italic magenta]I hope you like my little tool[/italic magenta] [bold green]▉[/bold green][bold white]▉[/bold white][bold red]▉[/bold red]")
    console.print("\nExiting ...", style="bold red")
    sys.exit()

def main():
    ascii_art_ians()
    show_options()
    while True:
        option = option_input()

        if option == 1:
            clear_screen()
            port_scan.Scanner().initialize()

        elif option == 2:
            sniffer_options()
            
        elif option == 3:
            clear_screen()
            ddos.initialize()

        elif option == 4:
            clear_screen()
            arper.initialize()

        elif option == 5:
            clear_screen()
            bruteforce.initialize()

        elif option == 6:
            clear_screen()
            trojan_creation.initialize()

        elif option == 7:
            chat_option()

        elif option == 8:
            mapper_options()

        elif option == 9:
            arp_a()

        elif option == 10:
            clear_screen()
            user_finder.initialize()

        elif option == 11:
            main()

        elif option == 12:
            show_info()

        elif option == 13:
            update()
            ascii_art_ians()
            show_options()

        else:
            exiting()
            
        main()

def mapper_options():
    console.print("\n[bold blue][1][/bold blue] if you have an open source site ")
    console.print("[bold blue][2][/bold blue] if you want to bruteforce file position ")
    console.print("[bold blue][3][/bold blue] to return to the menu ")
    option = int(console.input("\n┌── [[bold green]$ IANS $[/bold green]] ── [[bold red]mapper[/bold red]]:\n└───> "))
    while option not in (1, 2, 3):
        console.print("Invalid choice", style="italic yellow")
        option = int(console.input("\n┌── [[bold green]$ IANS $[/bold green]] ── [[bold red]mapper[/bold red]]:\n└───> "))
    clear_screen()
    if option == 1:
        mapper.initialize()
    elif option == 2:
        directory_bruter.initialize()
    else:
        main()

def option_input():
    try:
        option = int(console.input("\n┌── [[bold green]$ IANS $[/bold green]] ── [[bold red]main[/bold red]]:\n└───> "))
        while option > 14 or option < 1:
            console.print("Invalid choice", style="italic yellow")
            option = int(console.input("\n┌── [[bold green]$ IANS $[/bold green]] ── [[bold red]main[/bold red]]:\n└───> "))

    except ValueError:
        console.print("Invalid choice", style="italic yellow")
        option = option_input()

    return option

def show_info():
    clear_screen()
    print("\n")
    print("""
               boing         boing         boing              
 e-e           . - .         . - .         . - .          
(\_/)\       '       `.   ,'       `.   ,'       .        
 `-'\ `--.___,         . .           . .          .       
    '\( ,_.-'                                             
       \_\              "             " 

    """)

    console.print("[bold blue]Author[/bold blue]: Giovanni Iannaccone")
    console.print(f"[bold blue]Version[/bold blue]: {version}")
    console.print("\n[bold green]▉[/bold green][bold white]▉[/bold white][bold red]▉[/bold red]")

    console.print("""\nTool written for educational purpose only, the user know what he is doing 
and the author is not responsible for any malicious tool of IANS""", style="bold red")

    try:
        console.input("\n[red]Press [bold]Enter[/bold] to continue[/red] ")
    except KeyboardInterrupt:
        exiting()

    main()

def show_options():
    console.print("\n[bold blue][1][/bold blue] Port scanner\tfor port scanning")
    console.print("[bold blue][2][/bold blue] Sniffer\t\tfor sniffing ")
    console.print("[bold blue][3][/bold blue] DDos attack\t\tto start a DDos attack ")
    console.print("[bold blue][4][/bold blue] Arper\t\tfor ARP poisoning")
    console.print("[bold blue][5][/bold blue] Bruter\t\tfor bruteforce ")
    console.print("[bold blue][6][/bold blue] Trojan creator\tto create a trojan ")
    console.print("[bold blue][7][/bold blue] Chat ssh\t\tto create a ssh chat room ")
    console.print("[bold blue][8][/bold blue] Site mapper\t\tmap a site ")
    console.print("[bold blue][9][/bold blue] Arp-a\t\twho is connected to the router ")
    console.print("[bold blue][10][/bold blue] User finder\tfind username on social")

    console.print("\nNon hacking options:", style="italic")
    console.print("[bold blue][11][/bold blue] clear\tclear the terminal")
    console.print("[bold blue][12][/bold blue] info\tinfo on the tool")
    console.print("[bold blue][13][/bold blue] update\tupdate ians")
    console.print("[bold blue][14][/bold blue] exit\tbye bye :(")

def sniffer_options():
    console.print("\n[bold blue][1][/bold blue] for normal scan ")
    console.print("[bold blue][2][/bold blue] for email scanning ")
    console.print("[bold blue][3][/bold blue] for image scanning ")
    console.print("[bold blue][4][/bold blue] to return to the menu ")
    option = int(console.input("\n┌── [[bold green]$ IANS $[/bold green]] ── [[bold red]sniffer[/bold red]]:\n└───> "))
    while option not in (1, 2, 3, 4):
        console.print("Invalid choice", style="italic yellow")
        option = int(console.input("\n┌── [[bold green]$ IANS $[/bold green]] ── [[bold red]sniffer[/bold red]]:\n└───> "))
    clear_screen()
    if option == 1:
        sniffer.initialize()
    elif option == 2:
        mail_sniffer.initialize()
    elif option == 3:
        image_sniffer.initialize()
    else:
        main()

def update():
    os.system("chmod +x update.sh")
    os.system("./update.sh")

if __name__ == "__main__":
    console = Console()
    version = 1.0
    try:
        if os.name != "nt":
            os.system("chmod +x setup.sh")
            if os.system("./setup.sh") == 256:
                sys.exit(1)
        else:
            console.print("You are using windows os, this can cause some problems", style="bold red")
            time.sleep(2)
            
        clear_screen()
            
        ascii_art_warning()
        main()
    except KeyboardInterrupt:
        exiting()
