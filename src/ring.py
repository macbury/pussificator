import board
import neopixel
import time

COUNTDOWN_BG = (0, 0, 255)
COUNTDOWN_FG = (0, 255, 255)
SUCCESS_MIN = (0, 17, 0)
SUCCESS_MAX = (0, 255, 0)

CONNECTING_BG = (38, 22, 81)
CONNECTING_FG = (116, 66, 244)

EFFECT_CONNECTING = 'Connecting'
EFFECT_COUNTDOWN = 'Countdown'
EFFECT_SUCCESS = 'Success'
EFFECT_MANUAL = 'Manual'
EFFECT_NONE = 'None'

def lerp(progress, fromValue, toValue):
  return int((fromValue + (toValue - fromValue) * progress))

def lerpColor(progress, fromColor, toColor):
  return (
    lerp(progress, fromColor[0], toColor[0]),
    lerp(progress, fromColor[1], toColor[1]),
    lerp(progress, fromColor[2], toColor[2])
  )

class Ring:
  def __init__(self, pixelCount=16):
    self.pixelCount = 16
    self.pixels = neopixel.NeoPixel(board.D18, pixelCount, auto_write=False)
    self.clear()

  def clear(self):
    self.pixels.fill((0,0,0))
    self.pixels.show()

  def color(self, color, brightness):
    self.pixels.brightness = brightness
    self.pixels.fill(color)
    self.pixels.show()

  def pulse(self, colorMin, colorMax, ratio, up):
    self.pixels.brightness = 0.1
    t = ratio if up else 1 - ratio
    color = lerpColor(ratio, colorMin, colorMax)
    self.pixels.fill(color)
    self.pixels.show()

  def spinner(self, colorBg, colorFg, pos, spinnerWidth):
    self.pixels.brightness = 0.1
    self.pixels.fill(colorBg)

    for i in range(pos, pos + spinnerWidth):
      self.pixels[i % self.pixelCount] = colorFg

    self.pixels.show()

class RingController:
  def __init__(self):
    self.ring = Ring()
    self.progress = 0.0
    self.up = False
    self.step = 0.015
    self.counter = 0
    self.effect = EFFECT_NONE
    self.color = (255, 255, 255)
    self.brightness = 1.0

  def update(self):
    if self.progress == 1.0 or self.progress == 0.0:
      self.up = not self.up
    self.progress += self.step if self.up else -self.step
    self.progress = max(0.0, min(self.progress, 1.0))
    self.counter += 1
    self.counter %= self.ring.pixelCount

    if self.effect == EFFECT_MANUAL:
      self.ring.color(self.color, self.brightness)
    elif self.effect == EFFECT_CONNECTING:
      self.ring.spinner(CONNECTING_BG, CONNECTING_FG, self.counter, 2)
    elif self.effect == EFFECT_COUNTDOWN:
      self.ring.spinner(COUNTDOWN_BG, COUNTDOWN_FG, self.counter, 4)
    elif self.effect == EFFECT_SUCCESS:
      self.ring.pulse(SUCCESS_MIN, SUCCESS_MAX, self.progress, self.up)
    else:
      self.ring.clear()

    time.sleep(1.0/60.0)
