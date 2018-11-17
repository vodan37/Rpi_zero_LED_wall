import time
from frame_handler import *
import math
import colorsys
from vrtneopixel import *

# LED strip configuration:
LED_COUNT = 90      # Number of LED pixels.
LED_PIN = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10       # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(
    LED_COUNT,
    LED_PIN,
    LED_FREQ_HZ,
    LED_DMA,
    LED_INVERT,
    LED_BRIGHTNESS
)
# Intialize the library (must be called once before other functions).
strip.begin()




# Main program logic follows:
if __name__ == '__main__':

    for i in range( 0, strip.numPixels(), 1):                                     # iterate over all LEDs
        strip.setPixelColor( i, Color( 0, 0, 0 ) )                                # set LED to black (off)

    pic = [ Color(0,0,0) for x  in range(6*15)]

    handler = Rain(6, 15, rgb(150,10,10), rgb(50,50,50), 5000, 4)
    last_time = get_time_in_ms()

    while True:
        current_time = get_time_in_ms()

        if ((current_time - last_time) > 16):
            last_time = current_time

            frame = handler.next_frame(current_time)
            for i in range (6*15):
                pic[i] = Color(frame[i].r, frame[i].g, frame[i].b)

            for i in range( 0, strip.numPixels(), 1 ):                                # iterate over all LEDs
                strip.setPixelColor(                                                  # set pixel to color in picture
                    i,
                    pic[ i ]
                )
            strip.show()                                                              # update LEDs
            time.sleep(0.001)

        else:
            time.sleep(0.001)
