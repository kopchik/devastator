#!/usr/bin/env python3

from RPIO import PWM

from operator import itemgetter
from bisect import bisect_left
from threading import Thread
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


class Timer(Thread):
  def __init__(self, cb, timeout):
    self.cb = cb
    self.timeout = timeout
    read_fd, write_fd = os.pipe()
    self.read_fd = read_fd
    self.write_fd = write_fd

  def reset(self):
    os.write(self.write_fd, b'r')

  def cancel(self):
    os.write(self.write_fd, b'c')

  def schedule(self):
    while True:
      ready_fds = select.select([self.read],[],[], self.timeout)
      if self.read in ready_fds:
        mode = os.read(self.read_fd, 1)
        if mode == b'r':
          continue
        elif mode == b'c':
          break
        else:
          raise Exception("unknown mode %s" % mode)
      self.cb()


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

  def _set(self, v):
    v = int(v) // 10 * 10  # TODO: round to 10us
    self.servo.set_servo(self.pin, v)
    self.servo.stop_servo(self.pin)

  def reset(self):
    self._set(self.map[0])

  def set(self, value):
    pos = self.map[value]
    self._set(pos)

