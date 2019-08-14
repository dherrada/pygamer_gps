import time
import board
import busio
import digitalio

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

pressed = pad.get_pressed()

last_print = time.monotonic()
a = 0
while True:
    gps.update()

    current = time.monotonic()
    if current - last_print >= 1.0:
        last_print = current
        if not gps.has_fix:
            print('Waiting for fix...')
            continue

        pressed = pad.get_pressed()
        if pressed:
            a = pressed
        if a == 8:
            # longitude
            print('Longitude: {0:.6f} \ndegrees'.format(gps.longitude))
            print('\n\n\n\n\n')
            
        elif a == 4:
            # latitude
            print('Latitude: {0:.6f} \ndegrees'.format(gps.latitude))
            print('\n\n\n\n\n')

        elif a == 2:
            # datetime
            print('Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}'.format(
                gps.timestamp_utc.tm_mon,   # Grab parts of the time from the
                gps.timestamp_utc.tm_mday,  # struct_time object that holds
                gps.timestamp_utc.tm_year,  # the fix time.  Note you might
                gps.timestamp_utc.tm_hour,  # not get all data like year, day,
                gps.timestamp_utc.tm_min,   # month!
                gps.timestamp_utc.tm_sec))
            print('\n\n\n\n\n')

        elif a == 1:
            # speed
            if gps.speed_knots is not None:
                print('Speed: {} knots'.format(gps.speed_knots))
                print('\n\n\n\n\n\n')
        
        else:
            print("Red for longitude\nYellow for latitude\nBlack for datetime\nWhite for speed\n\n\n\n")
