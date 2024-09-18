import time
import socket
from   pytermx import Color

def url_to_ip(args, send, client):
    try:
        url = ""

        if len(args) == 2:
            url = args[1]
            host = str(url).replace("https://", "").replace("http://", "").replace("www.", "")

            ip = socket.gethostbyname(host)
            time.sleep(0.2)

            DATA_TEXT = f"URL {url} | IP {ip}"

            send(client, f"{Color.GREY}{DATA_TEXT}")
        else:
            send(client, Color.BRIGHT_RED + "!url_to_ip [URL]")
    except socket.gaierror:
        send(client, Color.BRIGHT_RED + "Invalid website.")