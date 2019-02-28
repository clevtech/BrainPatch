#!/usr/bin/env python3
from threading import Lock
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
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

port = port
percent = 0
starting = int(time.time())
averages = []


async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()


def background_thread():
    data = []
    s = serial.Serial(port, 115200)
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
                    percent2 = ((i/2000)*100)
                    socketio.emit('my_response',
                                  {'data': str(int(percent2)), 'count': "Calibrating"},
                                  namespace='/test')
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
                if percent > 20:
                    print("GO!")
                    averages.append(average)
                    socketio.emit('my_response',
                                  {'data': str(int(percent)), 'count': 'Go!'},
                                  namespace='/test')
                    urllib.request.urlopen("http://192.168.4.1/0")
                else:
                    print("STOP")
                    socketio.emit('my_response',
                                  {'data': str(int(percent)), 'count': 'Concentrate'},
                                  namespace='/test')
                    urllib.request.urlopen("http://192.168.4.1/1")
            except:
                average = value / float(len(data))
                # averages.append(average)
                pass
        except:
            s = serial.Serial(port, 115200)


# То что крутиться на заднем фоне



@socketio.on('connect', namespace='/test')
def test_connect():
    print("TEST")
    # global thread
    # with thread_lock:
    #     if thread is None:
    #         thread = socketio.start_background_task(target=background_thread)


@app.route('/')
def index():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)
    return render_template('dash.html', async_mode=socketio.async_mode)


@app.route('/go/')
def index2():
    urllib.request.urlopen("http://192.168.4.1/1")
    with thread_lock:
        if thread:
            socketio.stop()
    return render_template('index.html', async_mode=socketio.async_mode)


if __name__ == '__main__':
    socketio.run(app, debug=True)
