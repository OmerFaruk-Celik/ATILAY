from atilay import atilay
import time
master=atilay.set(0)
pwm=1300
a=1

while True:
	time.sleep(1)
	pwm+=a

	atilay.servo(7,pwm,master)
	if pwm<=1300:
		a=1
	elif pwm>=1600:
		a=-1
