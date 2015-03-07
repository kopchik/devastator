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
  xcam = MyServo(pin=13, map={-1: 2500, 0: 1600, +1: 700})
  ycam = MyServo(pin=5, map={-1: 2500, 0: 1400, +1: 700})
  rwheel = MyServo(pin=21, map={-1: 2500, 0: 1400, +1: 1600})
  lwheel = MyServo(pin=26, map={-1: 1600, 0: 1410, +1: 1200})

  DEBUG = False  # rpi may hang during reload


@post('/cam/set')
def cam():
  req = request.json
  print("got command", req)
  if gethostname() != 'alarmpi':
    return
  if 'look' in req:
    xcam.set(req['look'][0])
    ycam.set(req['look'][1])


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
