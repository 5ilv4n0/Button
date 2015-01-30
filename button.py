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

    def percent_play(self, percent, color=(255,255,255), alpha=0.5, dot=True):
        self.clear()
        led_count=12
        led_start=0
        if dot:
            led_count=11
            led_start=1
            dot_color = {'red':int(255*alpha),'green':int(255*alpha),'blue':int(0*alpha)}
            self[0] = dot_color
        brightness = int(8*alpha)
        percent = int( ((led_count*brightness)/100.0)*percent  )
        count = 0
        for led in range(led_start,12):
            for i in range(brightness):
                r = int((i*8)*(color[0]/255.0))
                g = int((i*8)*(color[1]/255.0))
                b = int((i*8)*(color[2]/255.0))
                self[led] = {'red':r,'green':g,'blue':b}
                print {'red':r,'green':g,'blue':b}
                if count == percent:
                    return
                count += 1
        return


    def percent_volume(self, percent, color=(0,255,255), alpha=0.5, dot=True):
        self.clear()
        led_count=7
        led_start=0
        if dot:
            led_count=6
            led_start=1
            dot_color = {'red':int(255*alpha),'green':int(255*alpha),'blue':int(255*alpha)}
            self[0] = dot_color

        real_percent = percent
        brightness = int(8*alpha)
        percent = int( ((led_count*brightness)/100.0)*percent  )

        count = 0
        for led in range(led_start,7):
            for i in range(brightness):
                r = int((i*8)*(color[0]/255.0))
                g = int((i*8)*(color[1]/255.0))
                b = int((i*8)*(color[2]/255.0))
                self[led] = {'red':r,'green':g,'blue':b}
                twin_led = (6-led)+6
                self[twin_led] = {'red':r,'green':g,'blue':b}

                print real_percent
                if real_percent == 100:
                    self[6] = {'red':255,'green':0,'blue':0}
                if count == percent:
                    return
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



class Kodi(XBMC):
    def __init__(self, api_url):
        self.api_url = api_url
        XBMC.__init__(self, api_url)


    def get_volume(self):
        out = self.Application.GetProperties(properties=["volume","muted"])
        print out
        return out['result']['volume']


button = Button()
button.clear()

kodi = Kodi("http://localhost:8080/jsonrpc")


volume_mem = 0
while True:
    volume = kodi.get_volume()
    if not volume == volume_mem:
        button.percent_volume(volume)
        button.update()
        volume_mem = volume

    time.sleep(0.1)





#method":"Application.GetProperties","params":{"properties":["volume"]}, id": 1}

#print kodi.Application.GetProperties(properties=["volume"])

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
