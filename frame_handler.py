import time
import random
from rgb import *

def get_time_in_ms():
    return (int(round(time.time() * 1000)))


def get_fade_color(start_color, destination_color, start_time, speed_in_ms, current_time):
    end_time = start_time+speed_in_ms
    adding_color = round(((rgb(destination_color.r - start_color.r, destination_color.g - start_color.g, destination_color.b - start_color.b))
                        /(end_time-start_time)*(current_time-start_time)))
    return (start_color+adding_color)

def normalize(pic):
    l = len(pic)
    frame = [ rgb( 0, 0, 0 ) for x in range( l ) ]
    for i in range(l):
        if ((pic[i].r) >= 255):
            frame[i].r = 255
        else:
            frame[i].r = pic[i].r

        if ((pic[i].g) >= 255):
            frame[i].g = 255
        else:
            frame[i].g = pic[i].g

        if ((pic[i].b) >= 255):
            frame[i].b = 255
        else:
            frame[i].b = pic[i].b
    return (frame)

class Handler:
    def next_frame(self, current_time):
        pass;


class Single_color_handler(Handler):
    def __init__(self, w, h, color):
        self.frame = [ rgb( color.r, color.g, color.b ) for x in range( w * h ) ]

    def next_frame(self, current_time):
        return self.frame

class Gradient(Handler):
    def __init__(self, w, h, colors, speed_in_ms):
        self.w = w
        self.h = h
        self.frame = [ rgb(colors[0].r, colors[0].g, colors[0].b) for x in range(w*h) ]
        self.speed_in_ms = speed_in_ms
        self.colors = colors
        self.start_time = get_time_in_ms()
        self.color_num = 1

    def next_frame(self, current_time):
        if (current_time > self.start_time + (self.color_num*self.speed_in_ms)):
            self.color_num = self.color_num + 1
        if (self.color_num >= len(self.colors)):
            self.reset()

        self.fading_color = self.colors[self.color_num-1]
        self.destination_color = self.colors[self.color_num]
        self.time_start_fading = self.start_time+self.speed_in_ms*(self.color_num-1)
        self.time_end_fading = self.start_time+self.speed_in_ms*(self.color_num)
        self.frame = [ get_fade_color(self.fading_color, self.destination_color, self.time_start_fading,
                                       self.speed_in_ms, current_time) for x in range(self.w * self.h) ]
        return (self.frame)

    def reset(self):
        self.start_time = get_time_in_ms()
        self.color_num = 1

class Random_pixels(Handler):
    def __init__(self, w, h, background, color, speed_in_ms):
        self.w = w
        self.h = h
        self.backgroud = background
        self.color = color
        self.speed_in_ms = speed_in_ms
        self.matrix = [[True, background, 0] for x in range(w * h)]
        self.last_time = get_time_in_ms()
        self.period = int((self.speed_in_ms/90)*(2.5+random.uniform(0,1)))
        self.frame = [ rgb( background.r, background.g, background.b ) for x in range( w * h ) ]

    def next_frame(self, current_time):
        if (current_time >= self.last_time + self.period):
            self.last_time = current_time
            self.period = int((self.speed_in_ms/90)*(2.5+random.uniform(0,1)))
            while(True):
                rand = random.randint(0,89)
                if(self.matrix[rand][0]):
                    self.matrix[rand][0] = False
                    self.matrix[rand][2] = current_time
                    break

        for i in range(90):
            if (self.matrix[i][0]):
                self.frame[i] = self.backgroud
            else:
                if (current_time <= (self.matrix[i][2]+self.speed_in_ms)):
                    self.frame[i] = get_fade_color(self.backgroud, self.color, self.matrix[i][2], self.speed_in_ms, current_time)
                else:
                    self.frame[i] = get_fade_color(self.color, self.backgroud, (self.matrix[i][2]+self.speed_in_ms), self.speed_in_ms, current_time)


        return (normalize(self.frame))


class Extrusion(Handler):

    def __init__(self, w, h, background, color, speed_in_ms):
        self.w = w
        self.h = h
        self.backgroud = background
        self.color = color
        self.speed_in_ms = speed_in_ms
        self.matrix = [[True, background, 0] for x in range(w * h)]
        self.last_time = get_time_in_ms()
        self.period = int(speed_in_ms/2.0)
        self.frame = [ rgb( background.r, background.g, background.b ) for x in range( w * h ) ]
        self.mode = "Forward"
        self.counter = 0

    def next_frame(self, current_time):
        if (current_time >= self.last_time + self.period):
            self.last_time = current_time
            while(True):
                rand = random.randint(0,89)
                if(self.matrix[rand][0]):
                    self.matrix[rand][0] = False
                    self.matrix[rand][2] = current_time
                    break

        for i in range(90):
            if (self.matrix[i][0]):
                self.frame[i] = self.backgroud
            else:
                if (current_time <= (self.matrix[i][2]+self.speed_in_ms)):
                    self.frame[i] = get_fade_color(self.backgroud, self.color, self.matrix[i][2], self.speed_in_ms, current_time)
                else:
                    self.frame[i] = self.color

        if (self.mode == "Forward" ):
            for i in range(self.w*self.h):
                if ((self.matrix[i][0]) == True):
                    self.counter= self.counter +1
            if (self.counter == 90):
                self.mode = "Back"
                self.counter = 0
                self.backgroud, self.color = self.color, self.backgroud
                for i in range(self.w*self.h):
                    self.matrix[i][0] = True
            else:
                self.counter = 0


        if (self.mode == "Back"):
            for i in range(self.w*self.h):
                if ((self.matrix[i][0]) == True):
                    self.counter= self.counter +1
            if (self.counter == 90):
                self.mode = "Forward"
                self.counter = 0
                self.backgroud, self.color = self.color, self.backgroud
                for i in range(self.w*self.h):
                    self.matrix[i][0] = True
            else:
                self.counter = 0

        return (normalize(self.frame))





