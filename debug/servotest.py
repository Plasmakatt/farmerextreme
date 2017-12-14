#!/usr/bin/python

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
p = GPIO.PWM(11,50)
p.start(7.5)

try:
    while True:
        # MID
        #p.ChangeDutyCycle(7.5)
        #time.sleep(1)
        # LEFT
        p.ChangeDutyCycle(20)
        time.sleep(1)
        # RIGHT
        p.ChangeDutyCycle(1)
        time.sleep(1)
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()
