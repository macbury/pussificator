import time
import json
from boot import CONFIG, LOGGER
from mqtt import MqttClient
import RPi.GPIO as GPIO

mqtt = MqttClient(CONFIG['mqtt'])
mqtt.start()

client.publish(MQTT_CONFIG['motion']['availability_topic'], 'on', 2)

try:
  while True:
    try:
      state = input()
      if not state:
        continue
      logger.info("Motion detected publishing to topic")
      client.publish(MQTT_CONFIG['motion']['state_topic'], 'on', 2)
    except EOFError:
      time.sleep(1)
except KeyboardInterrupt:
  pass
finally:
  client.publish(MQTT_CONFIG['motion']['availability_topic'], 'off', 2)