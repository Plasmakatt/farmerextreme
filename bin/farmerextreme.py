#!/usr/bin/python -Btt

import sys
import os
import time

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../lib")
print(os.path.dirname(os.path.realpath(__file__)) + "/../lib")

from servocontrol import ServoControl
from cameracontrol import CameraControl

START_QRCODE = "en.m.wikipedia"
STOP_QRCODE = "sv.wikipedia"
DIRECTION_LEFT = "left"
DIRECTION_RIGHT = "right"
STATE_START = "start"
STATE_STOP = "stop"
STATE_WORKING = "working"
state = STATE_WORKING

def work(camera_control, servo_control, scanned_qrcode, direction, state):
    qrcode = camera_control.get_qr_code()
    curr_state = STATE_WORKING
    if qrcode:        
        if qrcode not in scanned_qrcode:
            scanned_qrcode.append(qrcode)
            servo_control.move_stop()
            print('Found new qrcode, doing stuff here!')
            # Do some stuff here like watering etc.
            time.sleep(4)
            print('done doing stuff')
        elif is_at_pos(qrcode, STOP_QRCODE):
            print("is at stop")
            curr_state = STATE_STOP
        else:
            print('move servo, QRCODE ALREADY VISITED')
            if direction == DIRECTION_LEFT:
                servo_control.move_left()
            else:
                servo_control.move_right()
        print('return')
        return curr_state
    else:
        print(qrcode)

def move_to_start(camera_control, servo_control):
    while True:
        qrcode = camera_control.get_qr_code()
        if qrcode:
            print is_at_pos(qrcode, START_QRCODE) 
            if is_at_pos(qrcode, START_QRCODE):
                servo_control.move_stop()
                return STATE_START
            else:
                servo_control.move_right()
        else:
            servo_control.move_right()
        time.sleep(0.1)
    
def move_to_stop(camera_control, servo_control):
    while True:
        qrcode = camera_control.get_qr_code()
        if qrcode:
            print is_at_pos(qrcode, START_QRCODE) 
            if is_at_pos(qrcode, START_QRCODE):
                servo_control.move_stop()
                return STATE_STOP
            else:
                servo_control.move_left()
        else:
            servo_control.move_left()
        time.sleep(0.1)

def is_at_pos(qrcode, pos):
   print('is_at_pos')
   print qrcode
   print pos
   if qrcode != None:
       if pos in qrcode:
           print('At %s position' % pos)
           return True
   return False

def is_at_end(camera_control):
   qrcode = camera_control.get_qr_code()
   return is_at_pos(qrcode, STOP_QRCODE)

def is_at_start(camera_control):
   qrcode = camera_control.get_qr_code()
   return is_at_pos(qrcode, START_QRCODE)

def main():
    servo_control = ServoControl(11)
    servo_control.setup_gpio()
    camera_control = CameraControl()
    camera_control.start()
    try:
        camera_control.wait_for_camera()
        while True:
            scanned_qrcode = []
            if is_at_start(camera_control):
                # If at start we will work towards left
                print('is_at_start')
                direction = DIRECTION_LEFT
                state = STATE_START
            #elif is_at_end(camera_control):
            #    # If at the end we will work towards right
            #    print('is_at_end')
            #    direction = DIRECTION_RIGHT
            #    state = STATE_STOP
            else:
                # If not at start or not at end, move to start
                print('Not at start or end, moving to start')
                state = move_to_start(camera_control, servo_control)
                direction = DIRECTION_LEFT
                servo_control.move_stop()
            while True:
                curr_state = work(camera_control, servo_control, scanned_qrcode, direction, state)
                state = curr_state
                if state == STATE_STOP:
                    print('at stop')
                    break
                time.sleep(1)
    except KeyboardInterrupt:
        servo_control.stop()
        camera_control.stop()
        camera_control.join()

if __name__ == '__main__':
    main()
