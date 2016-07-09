#!/usr/bin/env python3
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

from operator import itemgetter
from bisect import bisect_left
from useful.timer import Timer
import atexit
import time


class Interpolate:
  # from http://stackoverflow.com/questions/7343697/linear-interpolation-python
  def __init__(self, X, Y):
    if any(y - x <= 0 for x, y in zip(X, X[1:])):
      raise ValueError("X must be in strictly ascending order!")
    self.X = X
    self.Y = Y
    intervals = zip(X, X[1:], Y, Y[1:])
    self.slopes = [(y2 - y1)/(x2 - x1) for x1, x2, y1, y2 in intervals]

  def __getitem__(self, x):
    i = bisect_left(self.X, x) - 1
    return self.Y[i] + self.slopes[i] * (x - self.X[i])



class MyServo:
  def __init__(self, name, pin, map, reset=True):
    X, Y = [], []
    for x, y in sorted(map.items(), key=itemgetter(0)):
      X.append(x)
      Y.append(y)
    self.map = Interpolate(X, Y)

    self.name = name
    self.pin = pin
    GPIO.setup(pin, GPIO.OUT)
    self.servo = GPIO.PWM(pin, 50)
    self.value = 0


    atexit.register(self.reset)
    atexit.register(self.stop)
    atexit.register(GPIO.cleanup)
    if reset:
      self.reset()
    #self.timer = Timer(self.stop, 1)
    #self.timer.start()

  def _set(self, v):
    self.servo.start(v)  #self.servo.ChangeDutyCycle(v)
    #self.timer.restart()
    # TODO: limit command rate because charger
    # cannot give enough power for two servos
    #time.sleep(0.1)

  def stop(self):
    self.servo.stop()

  def reset(self):
    self._set(self.map[0])

  def set(self, value):
    try:
      raw = self.map[value]
      self._set(raw)
      self.value = value
      print("{name} {val} {raw}\r".format(name=self.name, val=value, raw=raw))
    except IndexError:
      pass

  def inc(self, val):
    return self.set(self.value + val)

  def dec(self, val):
    return self.set(self.value - val)

  def reduce(self, value):
    if abs(self.value - value) <= value:
      self.set(0)
    else:
      if self.value > 0:
        self.dec(value)
      else:
        self.inc(value)
