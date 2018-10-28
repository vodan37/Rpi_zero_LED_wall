class rgb:
    def __init__(self, red, green, blue):
        self.r = red
        self.g = green
        self.b = blue

    def __add__(self, adding_coolor):
        return (rgb(self.r+adding_coolor.r, self.g+adding_coolor.g,self.b+adding_coolor.b))

    def __mul__(self, mul):
        return (rgb(self.r*mul,self.g*mul,self.b*mul))

    def __truediv__(self, div):
        return (rgb(self.r/div, self.g/div, self.b/div))

    def __round__(self, n=None):
        return (rgb(round(self.r), round(self.g), round(self.b)))

    def __str__(self):
        return("("+str(self.r)+"," +str(self.g) +"," + str(self.b) +")")
