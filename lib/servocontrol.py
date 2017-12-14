#!/usr/bin/python -Btt

import RPi.GPIO as GPIO
import time

class ServoControl:

    def __init__(self, gpio_pin):
        self.gpio_pin = gpio_pin

    def setup_gpio(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.gpio_pin, GPIO.OUT)
        print(self.gpio_pin)
        self.servo = GPIO.PWM(self.gpio_pin, 50)
        self.servo.start(7.5)

    def stop(self):
        self.servo.stop()
        GPIO.cleanup()

    def move_right(self):
        self.servo.ChangeDutyCycle(1)

    def move_left(self):
        self.servo.ChangeDutyCycle(20)

    def move_stop(self):
        self.servo.ChangeDutyCycle(0)
        
