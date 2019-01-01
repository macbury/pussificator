import RPi.GPIO as GPIO
from time import sleep

SERVO_PIN = 3

GPIO.setmode(GPIO.BOARD)
GPIO.setup(SERVO_PIN, GPIO.OUT)

pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(0)

def turnOff():
  GPIO.output(SERVO_PIN, False)
  pwm.ChangeDutyCycle(0)

def setAngle(angle):
  print("Set angle to: {}".format(angle))
  duty = angle / 18 + 2
  GPIO.output(SERVO_PIN, True)
  pwm.ChangeDutyCycle(duty)
  sleep(1)
  turnOff()

def feed():
  print("Feeding...")
  setAngle(180)
  setAngle(0)
  print("Feed Done...")

setAngle(0)
sleep(10)
try:
  while True:
    sleep(5)
    feed()
finally:
  pwm.stop()
  GPIO.cleanup()