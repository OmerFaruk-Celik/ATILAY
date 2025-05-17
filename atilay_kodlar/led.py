from gpiozero import LED
from time import sleep

led1 = LED(18)
led2 = LED(27)
led1.on()

while True:
    #led1.off()
    print("Led1 off")
    led1.off()
    sleep(0.5)
    led1.on()
    sleep(0.5)

