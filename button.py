#!/usr/bin/env python
# -*- coding: utf-8 -*-
import serial, os, time, sys

from xbmcjson import XBMC, PLAYER_VIDEO

class Button(dict):
    def __init__(self):
        dict.__init__(self)
        self.__device = serial.Serial('/dev/ttyACM0', 57600, timeout=1)
        self.clear()

    def percent(self, percent, color=(80,80,80)):
        self.clear()
        alpha = 1
        count = 0
        for led in range(12):
            for i in range(8):
                if count == percent:
                    return

                r = int((i*8)*alpha*(color[0]/255.0))
                g = int((i*8)*alpha*(color[1]/255.0))
                b = int((i*8)*alpha*(color[2]/255.0))
                #print (255/56)*r,(255/56)*g,(255/56)*b
                button[led] = {'red':r,'green':g,'blue':b}
                count += 1
        return

    def update(self):
        data = ''
        data += chr(self[1]['red'])+chr(self[1]['blue'])+chr(self[1]['green'])
        data += chr(self[0]['red'])+chr(self[0]['blue'])+chr(self[0]['green'])
        data += chr(self[11]['red'])+chr(self[11]['blue'])+chr(self[11]['green'])
        data += chr(self[10]['red'])+chr(self[10]['blue'])+chr(self[10]['green'])
        data += chr(self[9]['red'])+chr(self[9]['blue'])+chr(self[9]['green'])
        data += chr(self[8]['red'])+chr(self[8]['blue'])+chr(self[8]['green'])
        data += chr(self[7]['red'])+chr(self[7]['blue'])+chr(self[7]['green'])
        data += chr(self[6]['red'])+chr(self[6]['blue'])+chr(self[6]['green'])
        data += chr(self[5]['red'])+chr(self[5]['blue'])+chr(self[5]['green'])
        data += chr(self[4]['red'])+chr(self[4]['blue'])+chr(self[4]['green'])
        data += chr(self[3]['red'])+chr(self[3]['blue'])+chr(self[3]['green'])
        data += chr(self[2]['red'])+chr(self[2]['blue'])+chr(self[2]['green'])
        data += chr(10)
        self.__device.write(data)
        time.sleep(0.020)

    def clear(self,rgb=(0,0,0)):
        for i in range(12):
            self[i] = {'red':rgb[0],'green':rgb[1],'blue':rgb[2]}



button = Button()
button.clear()

#xbmc = XBMC("http://10.10.150.1:8080/jsonrpc")
#print xbmc.Player.GetProperties(playerid=1, properties=["percentage"])
#while True:
#    try:
#        percent = int(xbmc.Player.GetProperties(playerid=0, properties=["percentage"])['result']['percentage'])
#        print percent, '%'
#        button.percent(percent,(128,255,128))
#        button.update()
#    except:
#        try:
#            percent = int(xbmc.Player.GetProperties(playerid=1, properties=["percentage"])['result']['percentage'])
#            print percent, '%'
#            button.percent(percent,(128,255,128))
#            button.update()
#        except:
#            button.clear((2,16,2))
#            button.update()
#    time.sleep(0.25)



#while True:
#    for i in range(101):
#        button.percent(i,(128,128,128))
#        button.update()
    #time.sleep(0.75)

button.clear()
button.update()







while True:
    for i in range(12):
        button.clear((192,0,0))
        button[i]['red'] = 0
        button.update()
        time.sleep(0.10)
