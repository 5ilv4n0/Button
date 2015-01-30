#!/usr/bin/env python
# -*- coding: utf-8 -*-
import serial, os, time, sys

from xbmcjson import XBMC, PLAYER_VIDEO


class LED(object):
    def __init__(self, offset):
        self.__offset = offset
        self.__red = 0
        self.__green = 0
        self.__blue = 0

class Button(dict):
    def __init__(self):
        dict.__init__(self)
        self.__device = serial.Serial('/dev/ttyACM0', 57600, timeout=1)
        self.clear()

    def current_time(self):
        self.clear()
        h, m, s= os.popen('date +:%H:%M:%S:').read().split(':')[1:-1]
        h = int(h)
        if h>23:
            h=0
        m = int(m)
        s = int(s)
        if h > 11:
            h -= 12
        m = m / 5
        if m > 11:
            m = 0
        s = s / 5
        if s > 11:
            s = 0
        h -= 6
        m -= 6
        s -= 6
        if h <0:
            h = 12+h
        if m <0:
            m = 12+m
        if s <0:
            s = 12+s
        if s == h:
            self[s] = {'red':150,'green':0,'blue':20}
        else:
            self[s] = {'red':0,'green':0,'blue':20}
        if s == m:
            self[s] = {'red':0,'green':16,'blue':20}
        if h == m:
            color = {'red':20,'green':20,'blue':20}
            self[h] = color
        else:
            if not h == s:
                self[h] = {'red':150,'green':0,'blue':0}

            if not m == s:
                self[m] = {'red':0,'green':16,'blue':0}

    def percent(self, percent, color=(80,80,80)):
        self.clear()
        self[0] = {'red':80,'green':80,'blue':0}
        percent = int((87.0/100)*percent)
        print percent

        alpha = 1
        count = 0
        for led in range(1,12):
            for i in range(8):
                if count == percent:
                    return

                r = int((i*8)*alpha*(color[0]/255.0))
                g = int((i*8)*alpha*(color[1]/255.0))
                b = int((i*8)*alpha*(color[2]/255.0))
                #print (255/56)*r,(255/56)*g,(255/56)*b
                self[led] = {'red':r,'green':g,'blue':b}
                count += 1
        return


    def pulse(self, color=(80,80,80)):
        for alpha in range(32):
            a = alpha * 8
            for led in range(12):
                self[led] = {'red':a,'green':a,'blue':a}
            button.update()
        for alpha in range(32)[::-1]:
            a = alpha * 8
            for led in range(12):
                self[led] = {'red':a,'green':a,'blue':a}
            button.update()
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

xbmc = XBMC("http://localhost:8080/jsonrpc")

#method":"Application.GetProperties","params":{"properties":["volume"]}, id": 1}

print xbmc.Application.GetProperties(properties=["volume"])

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
