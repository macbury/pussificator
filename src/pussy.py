"""
Send as fast image capture over mqtt
"""
import time
import cv2
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
  ret, buf = cv2.imencode('.jpg', image)
  mqtt.publish(CONFIG['pussy']['topic'], buf.tobytes())

resolution = (1280, 720)
framerate = 5
stream = None
try:
  with PiCamera(resolution=resolution, framerate=framerate) as camera:
    stream = PiRGBArray(camera, size=resolution)
    LOGGER.info("Warming up camera")
    time.sleep(2)
    LOGGER.info("Starting capture...")
    for frame in camera.capture_continuous(stream, format='bgr', use_video_port=True):
      publish(frame.array)
      stream.truncate(0)
except KeyboardInterrupt:
  pass
finally:
  LOGGER.info("Exiting...")
  if stream:
    stream.truncate(0)