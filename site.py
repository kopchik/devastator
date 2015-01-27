#!/usr/bin/env python3

from bottle import abort, run, mount, load_app, default_app as app
from bottle import static_file, view
from bottle import get, post, request
from socket import gethostname
from subprocess import call, check_call
import atexit

DEBUG = True
if gethostname() == 'alarmpi':
  from myservo import MyServo
  xcam = MyServo(pin=13, map={-1: 2500, 0: 1400, +1: 700})
  ycam = MyServo(pin=5, map={-1: 2500, 0: 1600, +1: 700})
  DEBUG = False  # rpi may hang during reload


@post('/cam/set')
def cam():
  x,y = request.json
  print("set position to", x, y)
  if gethostname() != 'alarmpi':
    return
  xcam.set(x)
  ycam.set(y)


@get('/')
@view('main')
def index():
  return {}


@get('/static/<filename:path>')
def server_static(filename):
  return static_file(filename, root='static/')


if __name__ == '__main__':
  #check_call(["./pipeline.sh", "start"])
  #atexit.register(call, ["./pipeline.sh", "stop"])
  run(debug=DEBUG, interval=0.3, host='0.0.0.0', port=8080, reloader=DEBUG)
