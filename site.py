#!/usr/bin/env python3

from bottle import abort, run, mount, load_app, default_app as app
from bottle import static_file, view
from bottle import get, post, request
from socket import gethostname
from subprocess import call, check_call
import atexit

if gethostname() == 'alarmpi':
  from mymotor import MyMotor
  from myservo import MyServo

  xcam = MyServo(pin=24, map={-90: 2500, 0: 1400, +90: 700})
  ycam = MyServo(pin=23, map={-90: 2500, 0: 1600, +90: 700})
  motor = MyMotor(26, 19, 5)

@post('/cam/set')
def cam():
  xval = request.forms.get('xvalue')
  if xval:
    xcam.set_angle(int(xval))
  yval = request.forms.get('yvalue')
  if yval:
    ycam.set_angle(int(yval))
  return

@post('/cam/reset')
def cam():
  xcam.reset()
  ycam.reset()
  return

@post('/platform')
def platform():
  print(list(request.forms.items()))
  return

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
  run(debug=True, interval=0.3, host='0.0.0.0', port=8080, reloader=False)
