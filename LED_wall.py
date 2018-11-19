import serial
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
LED_W = 6
LED_H = 15

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

SERIALPORT = "/dev/ttyAMA0"
BAUDRATE = 115200

if __name__ == "__main__":
    ser = serial.Serial(SERIALPORT, BAUDRATE, timeout=0.001)
    handler = Single_color_handler(LED_W, LED_H, rgb(100,100,100))

    for i in range( 0, strip.numPixels(), 1):                                     # iterate over all LEDs
        strip.setPixelColor( i, Color( 0, 0, 0 ) )                                # set LED to black (off)

    pic = [ Color(0,0,0) for x  in range(LED_W*LED_H)]

    handler = Random_pixels(LED_W, LED_H, rgb(100,100,100), rgb(100,250,100), 3000)
    last_time = get_time_in_ms()

    while True:
        line = ser.readline().decode("utf-8")
        if (len(line) > 0):
            if(line[0]=="1"):     #single color
                handler = Single_color_handler(LED_W, LED_H, rgb(line[1:4], line[4:7], line[7:10]))

            if(line[0]=="2"):     #gradient
                num_of_colors = int(line[1])
                colors = []
                for x in range(num_of_colors):
                    colors.append(rgb(line[2+(9*x):5+(9*x)], line[5+(9*x):8+(9*x)], line[8+(9*x):11+(9*x)] ))

                speed = int(line[2+(9*num_of_colors):])

                handler = Gradient(LED_W, LED_H, colors, speed)

            if(line[0]=="3"):     #random pixels
                handler = Random_pixels(LED_W, LED_H, rgb(line[1:4],line[4:7],line[7:10]), rgb(line[10:13],line[13:16],line[16:19]), int(line[19:]))

            if(line[0]=="4"):     #extrusion
                handler = Extrusion(LED_W, LED_H, rgb(line[1:4],line[4:7],line[7:10]), rgb(line[10:13],line[13:16],line[16:19]), int(line[19:]))

            if(line[0]=="5"):     #rain
                handler = Rain(LED_W, LED_H, rgb(line[1:4],line[4:7],line[7:10]), rgb(line[10:13],line[13:16],line[16:19]), line[19], int(line[20:]))

            if(line[0]=="6"):     #tetris
                handler = Tetris(LED_W, LED_H, rgb(line[1:4],line[4:7],line[7:10]), rgb(line[10:13],line[13:16],line[16:19]), int(line[19:]))

            else:
                handler = Single_color_handler(LED_W, LED_H, rgb(0,0,0))

        current_time = get_time_in_ms()

        if ((current_time - last_time) > 16):
            last_time = current_time

            frame = handler.next_frame(current_time)
            for i in range (LED_W*LED_H):
                pic[i] = Color(int(frame[i].r), int(frame[i].g), int(frame[i].b))

            for i in range( 0, strip.numPixels(), 1 ):                                # iterate over all LEDs
                strip.setPixelColor(                                                  # set pixel to color in picture
                    i,
                    pic[ i ]
                )
            strip.show()


    ser.close()
