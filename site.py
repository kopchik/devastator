#!/usr/bin/env python3

from bottle import abort, run, mount, load_app, default_app as app
from bottle import static_file, view
from bottle import get, post, request


@post('/cam/set')
def cam():
  xval = request.forms.get('xvalue')
  yval = request.forms.get('yvalue')

  return

@post('/cam/reset')
def cam():
  return

@get('/')
@view('main')
def index():
  return {}

@get('/static/<filename:path>')
def server_static(filename):
    return static_file(filename, root='./static')


if __name__ == '__main__':
  run(debug=True, interval=0.3, host='0.0.0.0', port=8080, reloader=True)

