from multiprocessing import Process
import multiprocessing
import sys
import glob
import serial
import time
import urllib.request
import time
import matplotlib.pyplot as plt
import numpy

hl, = plt.plot([], [])


percent = 0
starting = int(time.time())


def update_line(hl, new_data):
    hl.set_xdata(numpy.append(hl.get_xdata(), new_data))
    hl.set_ydata(numpy.append(hl.get_ydata(), new_data))
    plt.draw()


def readValues(data):
    s = serial.Serial("/dev/tty.usbmodem411", 115200)
    print(s)
    while 1:
        raw = s.readline().strip().decode("utf-8")
        print(raw)
        if raw[0] == "{":
            raw = raw.split('{"d":[')[1]#.split(']}')[0]
            print(raw)
            data.append(raw)



def controlPet():
    data = []
    averages = []
    s = serial.Serial("/dev/tty.usbmodem641", 115200)
    print(s)
    global percent
    while 1:
        try:
            for i in range(100):
                while 1:
                    raw = s.readline().strip().decode("utf-8")
                    if raw[0] == "{":
                        raw = raw.split('"d":[')[1].split(']}')[0]
                        data.append(float(raw))
                        break
            value = 0
            for i in range(len(data)):
                value = value + abs(data[i])
            try:
                average = value / float(len(data))
                averages.append(average)
                percent = ((average - (sum(averages)/(len(averages)))/2)*100)
                now = int(time.time()) - starting
                print(percent)
                if percent > 80:
                    urllib.request.urlopen("http://192.168.4.1/0")
                else:
                    urllib.request.urlopen("http://192.168.4.1/1")
            except:
                pass
        except:
            s = serial.Serial("/dev/tty.usbmodem411", 115200)
