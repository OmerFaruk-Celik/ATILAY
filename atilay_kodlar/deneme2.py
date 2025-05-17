import cv2
import numpy as np
import socket
from atilay import atilay
from time import sleep

# Motor kontrol ayarları
master = atilay.set(0)
atilay.arm(master)
value=87
a=1
while True:
	value+=a
	atilay.ileri_geri(value)
	if value>=170:
		a=-1

	if value <10:
		a=1

	sleep(0.1)
