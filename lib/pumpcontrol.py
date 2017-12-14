#!/usr/bin/python -Btt

import RPi.GPIO as GPIO
import time

FIRST_PIN = 'MOTOR1A'
SECOND_PIN = 'MOTOR1B'
THIRD_PIN =  'MOTOR1C'

class PumpControl:

    def __init__(self, gpio_pins):
        self.gpio_pins = gpio_pins
        self._setup_pins()

    def _setup_pins(self):  
        GPIO.setup(self.gpio_pins[FIRST_PIN], GPIO.OUT)
        GPIO.setup(self.gpio_pins[SECOND_PIN], GPIO.OUT)
        GPIO.setup(self.gpio_pins[THIRD_PIN], GPIO.OUT)

    def turn_on_for_time(self, time_in_secs):
        self.turn_on()
        time.sleep(time_in_secs)


    def turn_on(self):
        GPIO.output(self.gpio_pins[FIRST_PIN], GPIO.HIGH)
        GPIO.output(self.gpio_pins[SECOND_PIN], GPIO.LOW)
        GPIO.output(self.gpio_pins[THIRD_PIN], GPIO.HIGH)

    def turn_off(self):
        GPIO.output(self.gpio_pins[FIRST_PIN], GPIO.HIGH)
        GPIO.output(self.gpio_pins[SECOND_PIN], GPIO.LOW)
        GPIO.output(self.gpio_pins[THIRD_PIN], GPIO.LOW)
