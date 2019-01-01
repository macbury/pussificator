import time
import json
from boot import CONFIG, LOGGER
from mqtt import MqttClient
from ring import RingController, EFFECT_CONNECTING, EFFECT_NONE

ring = RingController()
ring.effect = EFFECT_CONNECTING

mqtt = MqttClient(CONFIG['mqtt'])

def onCommandEvent(topic, body):
  LOGGER.info("Received: {}".format(body))
  if body['state'] == 'ON':
    if 'color' in body:
      color = body['color']
      ring.color = (
        int(color[r]),
        int(color[g]),
        int(color[b])
      )
    if 'brightness' in body:
      brightness = float(body['brightness'])/255.0
      ring.brightness = brightness
    ring.effect = body['effect'] if 'effect' in body else 'placeholder'
  else:
    ring.effect = EFFECT_NONE
  sendState()

def onConnect(mqtt):
  ring.effect = EFFECT_NONE
  sendState()

mqtt.onConnect = onConnect
mqtt.subscribe(CONFIG['light']['command_topic'], onCommandEvent)
mqtt.start()

def sendState():
  state = "OFF" if ring.effect == EFFECT_NONE else "ON"
  mqtt.publish(CONFIG['light']['state_topic'], json.dumps({
    "state": state,
    "brightness": ring.brightness,
    ""
  }))

try:
  LOGGER.info("Started!")
  while True:
    ring.update()
except KeyboardInterrupt:
  pass