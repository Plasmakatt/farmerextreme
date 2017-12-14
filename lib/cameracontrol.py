#!/usr/bin/python -Btt

import cv2
import time
import numpy
import zbar
from threading import Thread

CV_CACHE_COUNT = 5
LOOP_INTERVAL = 0.2

class CameraControl(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.scanner = zbar.ImageScanner()
        self.scanner.parse_config('enable')
        self.qrcode = None
        self.exit = False
        self.camera = cv2.VideoCapture(-1)

    def _start_capture(self):
        while not self.camera.isOpened():
            self.camera = cv2.VideoCapture(-1)

    def _scan(self, img):
        print "Scanning"
        # Convert image to gray
        grayed_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        raw_img = str(grayed_img.data)

        # Get image size
        width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        zbar_img = zbar.Image(width, height, 'Y800', raw_img)

        self.scanner.scan(zbar_img)
        data = ""
        for symbol in zbar_img:
            #print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
            data += str(symbol.data)
        return data

    def run(self):
        self._start_capture()
        while not self.exit:
            # Remove old imgs from cache
            for i in range(0, CV_CACHE_COUNT):
                self.camera.read()

            ret, img = self.camera.read()
            if ret == True:
                qrcode = self._scan(img)
                if qrcode:
                    self.qrcode = qrcode
            time.sleep(1)
        self.camera.release()

    def get_qr_code(self):
        qrcode = self.qrcode
        self.qrcode = None
        return qrcode

    def wait_for_camera(self):
        while not self.camera.isOpened():
            print "camera not yet started!"
            time.sleep(1)

    def stop(self):
        self.exit = True
