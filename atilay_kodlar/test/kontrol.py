from atilay import atilay
import time
d=atilay.lidar_on()
print(d)
for i in range(100):
	gx,gy,gz=atilay.hareket()
	print(gx,gy,gz)
	time.sleep(0.1)
