from rich.console import Console

import ipaddress
import os
import socket
import struct
import sys

class IP:
    def __init__(self, buff=None):
        header = struct.unpack("<BBHHHBBH4s4s", buff)
        self.ver = header[0] >> 4
        self.ihl = header[0] & 0xf

        self.tos = header[1]
        self.len = header[2]
        self.id = header[3]
        self.offset = header[4]
        self.ttl = header[5]
        self.protocol_num = header[6]
        self.sum = header[7]
        self.src = header[8]
        self.dst = header[9]

        self.src_address = ipaddress.ip_address(self.src)
        self.dst_address = ipaddress.ip_address(self.dst)

        self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except Exception as e:
            print("%s No protocol for %s" % (e, self.protocol_num))
            self.protocol = str(self.protocol_num)

class ICMP:
    def __init__(self, buff):
        header = struct.unpack("<BBHHH", buff)
        self.type = header[0]
        self.code = header[1]
        self.sum = header[2]
        self.id = header[3]
        self.seq = header[4]

def exiting(sniffer, sniffed_packets):
    console.print(f"\n[bold red]{sniffed_packets}[/bold red] packets were sniffed")
    if os.name == "nt":
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
    sys.exit(0)

def get_host_ip_addr(target):
    ip_addr = socket.gethostbyname(target)
    console.print(f"IP address for [bold red]{target}[/bold red] acquired: [bold blue]{ip_addr}[/bold blue]")
    return ip_addr

def main(addr):
    sniffed_packets = 0
    global console 
    console = Console()

    try:
        if os.name == "nt":
            socket_protocol = socket.IPPROTO_IP
        else:
            socket_protocol = socket.IPPROTO_ICMP

        sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
        sniffer.bind((get_host_ip_addr(addr), 0))
        sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        if os.name == "nt":
                sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

        while True:
            data = sniffer.recvfrom(65535)[0]
            ip_header = IP(data[0:20])

            console.print("[bold blue][+][/bold blue] Protocol: %s %s -> %s " % (ip_header.protocol, ip_header.src_address, ip_header.dst_address))
            console.print(f"Version: [bold blue]{ip_header.ver}[/bold blue]")
            console.print(f"Header Length: [bold blue]{ip_header.ihl}[/bold blue] TTL: [bold blue]{ip_header.ttl}[/bold blue]")

            if ip_header.protocol == "ICMP": 
                offset = ip_header.ihl * 4
                buf = data[offset:offset + 8]
                icmp_header = ICMP(buf)
                console.print(f"ICMP -> Type: %s Code: %s\n" % (icmp_header.type, icmp_header.code))

            sniffed_packets += 1

    except KeyboardInterrupt:
        exiting(sniffer, sniffed_packets)

    except OSError:
        exiting(sniffer, sniffed_packets)

if __name__ == "__main__":
    main(sys.argv[1])