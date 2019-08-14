import time
import board
import busio

import adafruit_gps

from math import pi,sqrt,sin,cos,atan2

RX = board.RX
TX = board.TX

uart = busio.UART(TX, RX, baudrate=9600, timeout=30)

gps = adafruit_gps.GPS(uart, debug=False)

gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')

gps.send_command(b'PMTK220,1000')

def haversine(lat1, lon1, lat2, lon2):

    degree_to_rad = float(pi / 180.0)

    d_lat = (lat2 - lat1) * degree_to_rad
    d_lon = (lon2 - lon1) * degree_to_rad

    a = pow(sin(d_lat / 2), 2) + cos(lat1 * degree_to_rad) * cos(lat2 * degree_to_rad) * pow(sin(d_lon / 2), 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    km = 6367 * c
    mi = 3956 * c

    return {"km":km, "miles":mi}

last_print = time.monotonic()

homelat = 38.888
homelon = -77.115
while True:
    gps.update()

    current = time.monotonic()
    if current - last_print >= 1.0:
        last_print = current
        if not gps.has_fix:
            print('Waiting for fix...')
            continue
        dist = haversine(gps.latitude, gps.longitude, homelat, homelon)
        print("Lat: {0:.6f}".format(gps.latitude))
        print("Lon: {0:.6f}\n".format(gps.longitude))
        print("You are: {0:.3f} km\nfrom home\n\nAnd: {1:.3f} miles\nfrom home".format(dist["km"], dist["miles"]))
