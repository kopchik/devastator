#!/usr/bin/env python3

from RPIO import PWM
from time import sleep
from sys import exit
import atexit

MIN, CENTER, MAX = 0,1,2

class MyServo:
  def __init__(self, pin, servo_range, angles):
    servo = PWM.Servo()

    self.servo = servo
    self.pin = pin
    self.servo_range = servo_range
    self.angles = angles
    atexit.register(self.reset)

    def set_pos(v, t):
      self.servo.set_servo(pin, v)
      sleep(t)
      servo.stop_servo(pin)
    self.set_pos = set_pos

  def reset(self):
    self.set_pos(self.servo_range[CENTER], 0.4)

  def set_angle(angle):
    

xcam = MyServo(pin=24, servo_range=[2500, 1400, 700], angles=[-90, 0, +90])
ycam = MyServo(pin=23, servo_range=[2500, 1600, 700], angles=[-90, 0, +90])
#cam.reset()
#cam.set_min()
#cam.set_max()
