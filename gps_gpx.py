import board
import busio
import digitalio

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

cs = digitalio.DigitalInOut(board.SD_CS)

import adafruit_sdcard
import storage

sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)

storage.mount(vfs, "/sd")

with open("/sd/test.txt", "w") as f:
    f.write("Hello World!\r\n")
