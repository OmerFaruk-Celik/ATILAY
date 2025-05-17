import RPi.GPIO as GPIO
import time
from time import sleep

GPIO.setmode(GPIO.BCM)
#Stop coming out Warnings
GPIO.setwarnings(False)

pinList = [2]
for i in pinList:
    GPIO.setup(pinList, GPIO.OUT)
