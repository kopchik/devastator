#!/usr/bin/env python3

from bottle import abort, run, mount, load_app, default_app as app
from bottle import static_file, view
from bottle import get, post, request

from myservo import MyServo

xcam = MyServo(pin=24, map={-90: 2500, 0: 1400, +90: 700})
ycam = MyServo(pin=23, map={-90: 2500, 0: 1600, +90: 700})

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

@get('/')
@view('main')
def index():
  return {}

@get('/static/<filename:path>')
def server_static(filename):
    return static_file(filename, root='./static')


if __name__ == '__main__':
  run(debug=True, interval=0.3, host='0.0.0.0', port=8080, reloader=False)

