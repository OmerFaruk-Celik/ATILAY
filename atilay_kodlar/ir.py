import RPi.GPIO as GPIO
import time

# declare the sensor and led pin
sensor_pin = 24
led_pin = 26

# GPIO setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor_pin, GPIO.IN)
GPIO.setup(led_pin, GPIO.OUT)

try:
    while True:
        
        if GPIO.input(sensor_pin):
            # If no object is near
            GPIO.output(led_pin, False)
            while GPIO.input(sensor_pin):
                #print(GPIO.input(sensor_pin))
                time.sleep(0.2)
        else:
            # If an object is detected
            GPIO.output(led_pin, True)
            print(GPIO.input(sensor_pin))
except KeyboardInterrupt:
    GPIO.cleanup()
