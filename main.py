from multiprocessing import Process
import multiprocessing
import sys
import glob
import serial
import time
import urllib.request
import time
from tqdm import tqdm
import random


percent = 0
starting = int(time.time())
averages = []



def controlPet():
    data = []
    s = serial.Serial("/dev/tty.usbmodem14101", 115200)
    print(s)
    global percent, averages
    print("Calibrating")
    for i in tqdm(range(2000)):
        while 1:
            try:
                raw = s.readline().strip().decode("utf-8")
                if raw[0] == "{":
                    raw = raw.split('"d":[')[1].split(']}')[0]
                    data.append(float(raw))
                    break
            except:
                pass
    value = 0
    for i in range(len(data)):
        value = value + abs(data[i])
    average = value / float(len(data))
    averages.append(average)

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

                percent = (((average - (sum(averages)/(len(averages))))/5)*100)
                # averages.append(average)
                now = int(time.time()) - starting
                print(percent)
                if percent < 0:
                    percent = random.random()*15
                    print(percent)
                if percent > 40:
                    print("GO!")
                    averages.append(average)
                    # urllib.request.urlopen("http://192.168.4.1/0")
                else:
                    print("STOP")
                    # urllib.request.urlopen("http://192.168.4.1/1")
            except:
                average = value / float(len(data))
                averages.append(average)
                pass
        except:
            s = serial.Serial("/dev/tty.usbmodem14101", 115200)


controlPet()
