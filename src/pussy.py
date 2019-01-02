import time
import json

import numpy
from cv2 import CascadeClassifier, cvtColor, COLOR_BGR2GRAY, imencode
from io import BytesIO
from picamera.array import PiRGBArray
from picamera import PiCamera
from boot import CONFIG, LOGGER
from mqtt import MqttClient

mqtt = MqttClient(CONFIG['mqtt'])
def onConnect(mqtt):
  LOGGER.info("Connected...")

mqtt.onConnect = onConnect
mqtt.start()

resolution = (800, 600)
framerate = 24
camera = PiCamera()
camera.resolution = resolution
camera.framerate = framerate
LOGGER.info("Warming up camera")
time.sleep(2)

stream = PiRGBArray(camera, size=resolution)
try:
  LOGGER.info("Starting capture...")
  for frame in camera.capture_continuous(stream, format='bgr', splitter_port = 2, resize = resolution, use_video_port=True):
    image = frame.array
    ret, buf = imencode('.jpg', image)
    mqtt.publish(CONFIG['pussy']['topic'], buf.tobytes())
    stream.truncate(0)
except KeyboardInterrupt:
  pass
finally:
  LOGGER.info("Exiting...")
  camera.close()
  stream.truncate(0)