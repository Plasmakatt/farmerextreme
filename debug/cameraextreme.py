#!/usr/bin/python -Btt

import sys
import os
import time

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../lib")
print(os.path.dirname(os.path.realpath(__file__)) + "/../lib")

from cameracontrol import CameraControl

def main():
    try:
        camera_control = CameraControl()
        camera_control.start()
        while True:
            qrcode = camera_control.get_qr_code()
            if qrcode:
                print qrcode
            time.sleep(1)
    except KeyboardInterrupt:
        camera_control.stop()
        camera_control.join()

if __name__ == '__main__':
    main()
