import atexit
import RPIO

class MyMotor:
  def __init__(self, enable, ff, rw):
    RPIO.setup(enable, RPIO.OUT)
    RPIO.setup(ff, RPIO.OUT)
    RPIO.setup(rw, RPIO.OUT)
    self.enable = enable
    self.ff = ff
    self.rw = rw
    atexit.register(self.stop)

  def stop(self):
    RPIO.output(self.enable, False)

  def go_ff(self):
    RPIO.output(self.rw, False)
    RPIO.output(self.enable, True)
    RPIO.output(self.ff, True)

  def go_rw(self):
    RPIO.output(self.ff, False)
    RPIO.output(self.enable, True)
    RPIO.output(self.rw, True)


