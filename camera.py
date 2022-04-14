from picamera import PiCamera
import time
camera = PiCamera()
camera.resolution = (640, 480)
camera.vflip = True
counter = 1
while(1==1):
    camera.start_preview()
    time.sleep(2)
    camera.capture("Data/foto"+str(counter)+".jpg")
    camera.stop_preview()
    counter+=1
    time.sleep(3600)
