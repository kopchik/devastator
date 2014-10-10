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
    self.servo = PWM.Servo()
    self.pin = pin
    self.servo_min = servo_min
    self.servo_max = servo_max
    self.servo_center = servo_center
    atexit.register(self.reset)
  def reset(self):
    self.servo.set_servo(self.pin, self.servo_center)
    sleep(0.4)
    self.servo.stop_servo(self.pin)

xcam = Cam(pin=24, servo_min=2500, servo_max=690, servo_center=1600)
ycam = Cam(pin=24, servo_min=2500, servo_max=690, servo_center=1600)
xcam.reset()
