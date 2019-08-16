import time
import board
import busio
import digitalio
import analogio
from math import pi,sqrt,sin,cos,atan2

from gamepadshift import GamePadShift

import adafruit_gps

RX = board.RX
TX = board.TX

uart = busio.UART(TX, RX, baudrate=9600, timeout=30)

gps = adafruit_gps.GPS(uart, debug=False)

gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')

gps.send_command(b'PMTK220,1000')

pad = GamePadShift(digitalio.DigitalInOut(board.BUTTON_CLOCK),
                   digitalio.DigitalInOut(board.BUTTON_OUT),
                   digitalio.DigitalInOut(board.BUTTON_LATCH))

joystick_x = analogio.AnalogIn(board.JOYSTICK_X)
joystick_y = analogio.AnalogIn(board.JOYSTICK_Y)

pressed = pad.get_pressed()
select = 0
b = 0

last_print = time.monotonic()
a = 0

homelat = 38.888
homelon = -77.115

def haversine(lat1, lon1, lat2, lon2):

     degree_to_rad = float(pi / 180.0)

     d_lat = (lat2 - lat1) * degree_to_rad
     d_lon = (lon2 - lon1) * degree_to_rad

     a = pow(sin(d_lat / 2), 2) + cos(lat1 * degree_to_rad) * cos(lat2 * degree_to_rad) * pow(sin(d_lon / 2), 2    )
     c = 2 * atan2(sqrt(a), sqrt(1 - a))
     km = 6367 * c
     mi = 3956 * c
 
     return {"km":km, "miles":mi}

while True:
    gps.update()

    current = time.monotonic()
    if current - last_print >= 0.2:
        last_print = current
        if not gps.has_fix:
            print('Waiting for fix...')
            continue
        if joystick_y.value > 37000 and a < 5:
            a += 1
        elif joystick_y.value < 28000 and a > 0:
            a -= 1
        if not b:
            array = [' ', ' ', ' ', ' ', ' ', ' ']
            array.insert(a, '*')
            print("{0}Farfromhome\n{1}Longitude\n{2}Latitude\n{3}Datetime\n{4}Speed\n{5}Altitude".format(array[0], array[1], array[2], array[3], array[4], array[5]))
            print("\n")
        if joystick_x.value > 37000:
            b = 1
        elif joystick_x.value < 28000:
            b = 0
        if b:
            if a == 0:
                # farfromhome
                 dist = haversine(gps.latitude, gps.longitude, homelat, homelon)
                 print("Lat: {0:.6f}".format(gps.latitude))
                 print("Lon: {0:.6f}\n".format(gps.longitude))
                 print("You are: {0:.3f} km\nfrom home\n\nAnd: {1:.3f} miles\nfrom home".format(dist["km"], dist["miles"]))
 
            elif a == 1:
                # longitude
                print('Longitude: {0:.6f} \ndegrees'.format(gps.longitude))
                print('\n\n\n\n\n')
                
            elif a == 2:
                # latitude
                print('Latitude: {0:.6f} \ndegrees'.format(gps.latitude))
                print('\n\n\n\n\n')

            elif a == 3:
                # datetime
                print('Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}'.format(
                    gps.timestamp_utc.tm_mon,   # Grab parts of the time from the
                    gps.timestamp_utc.tm_mday,  # struct_time object that holds
                    gps.timestamp_utc.tm_year,  # the fix time.  Note you might
                    gps.timestamp_utc.tm_hour,  # not get all data like year, day,
                    gps.timestamp_utc.tm_min,   # month!
                    gps.timestamp_utc.tm_sec))
                print('\n\n\n\n\n')

            elif a == 4:
                # speed
                if gps.speed_knots is not None:
                    print('Speed: {} knots'.format(gps.speed_knots))
                    print('Speed: {} mph'.format(gps.speed_knots*1.151))
                    print('speed: {} kmh'.format(gps.speed_knots*1.852))
                    print('\n\n\n\n')
            elif a == 5:
                # altitude
                print('Altitude: {} meters'.format(gps.altitude_m))
                print('Altitude: {} feet'.format(gps.altitude_m * 3.28084))
                print('\n\n\n\n\n')
