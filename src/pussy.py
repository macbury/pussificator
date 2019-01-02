import time
import json
import numpy
import cv2

from cv2 import CascadeClassifier, cvtColor, COLOR_BGR2GRAY, imencode, CascadeClassifier
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

def publish(image):
  LOGGER.info("Sending")
  ret, buf = imencode('.jpg', image)
  mqtt.publish(CONFIG['pussy']['topic'], buf.tobytes())

def detect(image):
  LOGGER.info("Detecting")
  pussies = pussyCascade.detectMultiScale(image, scaleFactor=1.3, minNeighbors=10)
  LOGGER.info("Done")
  for (x, y, w, h) in pussies:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    LOGGER.info("Found a puss")
  return image

resolution = (1280, 720)
framerate = 2
stream = None
LOGGER.info("Loading model...")
pussyCascade = CascadeClassifier('haarcascade_frontalcatface_extended.xml')
try:
  with PiCamera(resolution=resolution, framerate=framerate) as camera:
    stream = PiRGBArray(camera, size=resolution)
    LOGGER.info("Warming up camera")
    time.sleep(2)
    LOGGER.info("Starting capture...")
    for frame in camera.capture_continuous(stream, format='bgr', splitter_port = 2, use_video_port=True):
      LOGGER.info("Captured!")
      image = detect(frame.array)
      publish(image)
      stream.truncate(0)
except KeyboardInterrupt:
  pass
finally:
  LOGGER.info("Exiting...")
  if stream:
    stream.truncate(0)