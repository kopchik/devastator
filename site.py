#!/usr/bin/env python3

from bottle import abort, run, mount, request, load_app, default_app as app
from bottle import static_file, view
from bottle import get

@get('/')
@view('main')
def index():
  return {'x':"HABA"}

@get('/static/<filename:path>')
def server_static(filename):
    return static_file(filename, root='./static')


if __name__ == '__main__':
  run(debug=True, interval=0.3, host='0.0.0.0', port=8080, reloader=True)

