import time
import wpilib
from magicbot import tunable
from wpilib import AddressableLED
k_numberLEDs = 25

class Light:

    def setup(self):
         #Instantiate an LED Object on PWM pin 9.
        self.led = AddressableLED(9)
        #set the number of leds
        self.led.setLength(k_numberLEDs)
        #Create an LED Data Object for the left side
        self.left = wpilib.AddressableLED.LEDData(255, 0, 0)  # I could not get this to instantiate without passing a color.
        
        #Set the length of the led strip 
        self.led.setData([self.left] * k_numberLEDs)
        #Fill the buffer with color
        #self.left.setRGB(red_led,green_led,blue_led)
        self.left.setRGB(0, 0, 0)
        # self.left.setRGB(250, 90, 10)
        # Write the buffer to the strip
        self.led.setData([self.left]*k_numberLEDs)

        #start the strip lighting
        #self.led.start()

        #data = [wpilib.AddressableLED.LEDData(255, 0, 0) for _ in range(26)]

        #for d in data:
        #    d.setRGB(0,255,0)

        #data[0].setRGB(255,0,0)    
        #data[1].setRGB(255,80,10)
        #data[2].setRGB(227,255,0)
        #data[3].setRGB(0,255,0)
        #data[4].setRGB(0,0,255)
        #data[5].setRGB(255,0,255)
        #data[6].setRGB(255,0,0)    
        #data[7].setRGB(255,80,10)
        #data[8].setRGB(227,255,0)
        #data[9].setRGB(0,255,0)
        #data[10].setRGB(0,0,255)
        #data[11].setRGB(255,0,255)
        #data[12].setRGB(255,0,0)    
        #data[13].setRGB(255,80,10)
        #data[14].setRGB(227,255,0)
        #data[15].setRGB(0,255,0)
        #data[16].setRGB(0,0,255)
        #data[17].setRGB(255,0,255)
        #data[18].setRGB(255,0,0)    
        #data[19].setRGB(255,80,10)
        #data[20].setRGB(227,255,0)
        #data[21].setRGB(0,255,0)
        #data[22].setRGB(0,0,255)
        #data[23].setRGB(255,0,255)
        #data[24].setRGB(255,0,0)    
        #data[25].setRGB(255,80,10)

        #self.led.setData(data)
        
        #self.led.start()

        #rainbow = 0
        #data = [wpilib.AddressableLED.LEDData(255, 0, 0) for _ in range(26)]
        #for d in data:
        #    d.setRGB(rainbow,0,255)
        #    d +=1
        #    if rainbow > 255:
        #        rainbow = 0
        #    rainbow += 3
        #self.led.setData(data)P
        #self.led.start()

    def execute(self):
        self.led.start()

    def darken(self):
        self.left.setRGB(0, 0, 0)
        self.led.setData([self.left]*k_numberLEDs)
        self.led.start()
        
    def reden(self):
        self.left.setRGB(10, 0, 0)
        self.led.setData([self.left]*k_numberLEDs)
        self.led.start()
        
    def greenen(self):
        self.left.setRGB(0, 10, 0)
        self.led.setData([self.left]*k_numberLEDs)
        self.led.start()

    #def setColor(self, color):
    #    #AVAILABLE COLORS: red, blue, orange, green, white
    #    if color == "red":
    #        self.left.setRGB(255, 0, 0)
    #    elif color == "green":
    #        self.left.setRGB(0, 255, 0)
    #    elif color == "blue":
    #        self.left.setRGB(0, 0, 255)
    #    elif color == "orange":
    #        self.left.setRGB(255, 80, 10)
    #    elif color == "white":
    #        self.left.setRGB(255, 255, 255)
    #    self.led.setData([self.left]*k_numberLEDs)
    #    self.led.start()
