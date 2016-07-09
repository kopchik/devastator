#!/usr/bin/env python3
import atexit

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

from useful.libgui import myinput, mywrapper, ARROW
from myservo import MyServo


@mywrapper
def main():
  xcam = MyServo(name="xcam", pin=13, map={-1: 4.6, 0: 6.8, +1: 8.6})
  ycam = MyServo(name="ycam", pin=5, map={-1: 9.8, 0: 5.2, +1: 2.7})
  lwheel = MyServo(name="lwheel", pin=21, map={-1: 7.9, 0: 6.85, +1: 5.8})
  rwheel = MyServo(name="rwheel", pin=26, map={-1: 5.8, 0: 6.85, +1: 7.9})


  for key in myinput(timeout=1.0):
    print(key, '\r')

    # wheels
    if key is None:
      rwheel.reduce(0.05)
      lwheel.reduce(0.05)
    if key == 'w':
      lwheel.dec(0.1)
      rwheel.dec(0.1)
    elif key == 's':
      lwheel.inc(0.1)
      rwheel.inc(0.1)
    elif key == 'd':
      rwheel.inc(0.1)
    elif key == 'a':
      lwheel.inc(0.1)

    # cam
    if key == ARROW.LEFT:
      xcam.inc(0.1)
    elif key == ARROW.RIGHT:
      xcam.dec(0.1)
    elif key == ARROW.UP:
      ycam.inc(0.1)
    elif key == ARROW.DOWN:
      ycam.dec(0.1)
    elif key in ['q', 'Q']:
      return

if __name__ == '__main__':
  main()
