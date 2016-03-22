import picamera
import time

camera = picamera.PiCamera()

while 1 == 1:
    camera.capture('/home/pi/controlapp/static/snapshot.jpg')
    print 'took picture'
    time.sleep(5)
