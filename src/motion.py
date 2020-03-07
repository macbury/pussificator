import time
import json
from boot import CONFIG, LOGGER
from mqtt import MqttClient
import RPi.GPIO as GPIO

mqtt = MqttClient(CONFIG['mqtt'])
def onConnect(mqtt):
  LOGGER.info("connected!")

mqtt.onConnect = onConnect
mqtt.start()

availability_topic = CONFIG['motion']['availability_topic']
state_topic = CONFIG['motion']['state_topic']
mqtt.publish(availability_topic, 'on')
LOGGER.info("Sending to topic info {}".format(availability_topic))

try:
  while True:
    try:
      state = input()
      if not state:
        continue
      if state == 'cat':
        LOGGER.info("Motion detected publishing to topic {}".format(state_topic))
        mqtt.publish(state_topic, 'on')
    except EOFError:
      time.sleep(1)
except KeyboardInterrupt:
  pass
finally:
  mqtt.publish(availability_topic, 'off')