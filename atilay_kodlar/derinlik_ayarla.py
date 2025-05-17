from atilay import atilay
import time
#master=atilay.set(0)

def set_pwm(pwm=1511):
	dosya=open("/home/rasp/atilay/derinlik","r")
	derinlik=dosya.read()
	dosya.close()
	try:
		derinlik=int(derinlik)
		mevcut_d=int(atilay.lidar("z"))
		#print(mevcut_d)
		if mevcut_d > derinlik + 5:
			fark=mevcut_d-derinlik
			pwm=1511-2*fark-10
			if pwm<=1200:
				pwm=1200
		elif mevcut_d < derinlik - 5:
			fark=derinlik-mevcut_d
			pwm=1511+2*fark+10
			if pwm>=1600:
				pwm=1600


	except:
		pwm=1511
		
	return pwm


pwm=1511
while True:
	time.sleep(0.2)
	pwm=set_pwm()

	atilay.bat_cik(pwm)
	print(pwm)






