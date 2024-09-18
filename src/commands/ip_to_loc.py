import requests
from   pytermx import Color

def get_location(ip_addr):
    ip_address = ip_addr
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    version = response.get("version")
    city = response.get("city")
    region_city = response.get("region")
    country_name = response.get("country_name")
    latitude = response.get("latitude")
    longitude = response.get("longitude")
    timezone = response.get("timezone")
    network = response.get("network")

    location_data = f'''IP            : {ip_address}
NETWORK       : {network}
VERSION       : {version}

# LOCATION
CITY          : {city}
REGION        : {region_city}
COUNTRY       : {country_name}
LATITUDE      : {latitude}
LONGITUDE     : {longitude}

# TIME
TIMEZONE      : {timezone}'''

    return location_data

def ip_to_loc(args, send, client):
    try:
        ip = ""

        if len(args) == 2:
            ip = str(args[1])
            ip_location = get_location(ip)
            
            DATA_TEXT = f'{ip_location}'

            for x in DATA_TEXT.splitlines():
                send(client, f"{Color.GREY}{x}")
        else:
            send(client, Color.BRIGHT_RED + "!ip_to_loc [IP]")
    except:
        send(client, Color.BRIGHT_RED + "Invalid data.")