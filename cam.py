#!/usr/bin/env python3

from RPIO import PWM
from time import sleep
from sys import exit
import atexit

XCAM = 24
MIN_DOWN = 2500
MAX_UP = 690
VERT_CENTER = 1600

YCAM = 23

class Cam:
  def __init__(self, pin, servo_min, servo_max, servo_center):
    servo = PWM.Servo()

    self.servo = servo
    self.pin = pin
    self.servo_min = servo_min
    self.servo_max = servo_max
    self.servo_center = servo_center
    atexit.register(self.reset)

    def set_pos(v, t):
      self.servo.set_servo(pin, v)
      sleep(t)
      servo.stop_servo(pin)
    self.set_pos = set_pos

  def reset(self):
    self.set_pos(self.servo_center, 0.4)

  def set_min(self):
    self.servo.set_servo(self.pin, self.servo_min)
    sleep(2)
    self.servo.stop_servo(self.pin)

  def set_max(self):
    self.servo.set_servo(self.pin, self.servo_max)
    sleep(2)
    self.servo.stop_servo(self.pin)


cam = Cam(pin=24, servo_min=2500, servo_max=700, servo_center=1400)
cam = Cam(pin=23, servo_min=2500, servo_max=700, servo_center=1600)
#cam.reset()
#cam.set_min()
#cam.set_max()
