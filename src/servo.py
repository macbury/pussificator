import time
import json
from boot import CONFIG, LOGGER
from mqtt import MqttClient
import RPi.GPIO as GPIO

mqtt = MqttClient(CONFIG['mqtt'])

SERVO_PIN = 3

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
  turnOff()

def feed():
  LOGGER.info("Feeding...")
  setAngle(180)
  setAngle(0)
  LOGGER.info("Feed Done...")

def onCommandEvent(topic, body):
  LOGGER.info("Received: {}".format(body))
  feed()

def onConnect(mqtt):
  LOGGER.info("Connected!")

mqtt.onConnect = onConnect
mqtt.subscribe(CONFIG['servo']['command_topic'], onCommandEvent)
mqtt.start()

try:
  LOGGER.info("Started!")
  setAngle(0)
  while True:
    time.sleep(1)
except KeyboardInterrupt:
  pass