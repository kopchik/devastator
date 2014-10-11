#!/usr/bin/env python3

from RPIO import PWM

from operator import itemgetter
from bisect import bisect_left
from time import sleep
from sys import exit
import atexit


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
  def __init__(self, pin, map):
    X, Y = [], []
    for x, y in sorted(map.items(), key=itemgetter(0)):
      X.append(x)
      Y.append(y)
    self.map = Interpolate(X, Y)

    self.servo = PWM.Servo()
    self.pin = pin
    atexit.register(self.reset)

    def set_pos(v, t):
      self.servo.set_servo(pin, v)
      sleep(t)
      servo.stop_servo(pin)
    self.set_pos = set_pos

  def reset(self):
    self.set_pos(self.map[0], 0.5)

  def set_angle(self, angle):
    pos = self.map[angle]
    self.set_pos(pos, t=0.4)

