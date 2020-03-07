import time
import json
from boot import CONFIG, LOGGER
from mqtt import MqttClient
import RPi.GPIO as GPIO

mqtt = MqttClient(CONFIG['mqtt'])

SERVO_PIN = 12

GPIO.setmode(GPIO.BOARD)
GPIO.setup(SERVO_PIN, GPIO.OUT)

pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(0)

def turnOff():
  GPIO.output(SERVO_PIN, False)
  pwm.ChangeDutyCycle(0)

def setAngle(angle):
  LOGGER.info("Set angle to: {}".format(angle))
  duty = angle / 18 + 2
  GPIO.output(SERVO_PIN, True)
  pwm.ChangeDutyCycle(duty)
  time.sleep(1)

def feed():
  LOGGER.info("Moving fan to fill state...")
  setAngle(0)
  time.sleep(1)
  LOGGER.info("Moving fan to extract state...")
  setAngle(180)
  time.sleep(1)

def neutral():
  LOGGER.info("Moving fan back to neutral state...")
  setAngle(90)
  time.sleep(1)
  LOGGER.info("Feed Done...")

def onCommandEvent(topic, body):
  LOGGER.info("Received: {}".format(body))
  feed()
  neutral()
  turnOff()

def onConnect(mqtt):
  LOGGER.info("Connected!")

mqtt.onConnect = onConnect
mqtt.subscribe(CONFIG['servo']['command_topic'], onCommandEvent)
mqtt.start()

try:
  LOGGER.info("Started!")
  neutral()
  while True:
    time.sleep(1)
except KeyboardInterrupt:
  pass