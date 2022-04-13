import imp
from gpiozero import AngularServo
from time import sleep

servo =AngularServo(18, min_angle=0, max_angle=270, min_pulse_width=0.0005, max_pulse_width=0.0025)

while (True):
    servo.angle = 0
    sleep(2)
    servo.angle = 135
    sleep(2)
    servo.angle = 260
    sleep(2)
    