from time import monotonic, sleep

import adafruit_tsl2591
import board
import microcontroller
import usb_cdc
from neopixel import NeoPixel
from rainbowio import colorwheel

sensor = adafruit_tsl2591.TSL2591(board.i2c())
serial = usb_cdc.data
pixels = NeoPixel(board.NEOPIXEL, 1, brightness=0.4)

colours = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "cyan": (0, 255, 255),
    "purple": (255, 0, 255),
    "yellow": (255, 255, 0),
    "white": (255, 255, 255),
    "off": (0, 0, 0)
    }

def clear_pixels():
    pixels.fill(colours["off"])
    pixels.show()

def blink(colour="green", n=3):
    clear_pixels()
    for _ in range(n):
        pixels.fill(colours[colour])
        pixels.show()
        sleep(0.5)
        clear_pixels()
        sleep(0.5)

def buffer_cycle(colour="blue"):
    pixels.fill(colours[colour])
    pixels.show()
    sleep(0.2)
    clear_pixels()

def wait_for_connection():
    while not serial.connected:
        buffer_cycle()
    blink("green", n=1)
    # serial.write(b'connected')

def get_light():
    light = sensor.lux #lux
    vis = sensor.visible
    ir = sensor.infrared
    return light, vis, ir

def get_temp() -> str:
    t = microcontroller.cpu.temperature
    return f"{t}°C"

def main():
    clear_pixels()
    wait_for_connection()

    while serial.connected:
        pixels.fill(colorwheel((monotonic()*50)%255) )
        time.sleep(0.05)
        txt = ','.join([str(i) for i in get_light()]) + ',' + get_temp()
        msg = bytearray(text, 'utf-8')
        serial.write(msg)
        sleep(3)
    main()


if __name__ == '__main__':
    main()
