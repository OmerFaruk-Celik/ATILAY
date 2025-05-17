
# -*- coding: utf-8 -*
from pymavlink import mavutil
import time
import serial
# Create the conn

def set(a=0):
        master = serial.Serial("/dev/ttyACM"+str(a),9600)
        return master


def send_value_to_arduino(motor_num, value,master=set(0)):
    command = f"{motor_num},{value}\n"
    master.write(command.encode())  # Komutu Arduino'ya gönder


def buzzer_play(master=set(0)):
    # Pixhawk arming melodisi için frekans ve süre bilgileri
    pixhawk_melody = [
        (3568, 100),  # G6
        (3047, 100),  # C6
        (3319, 100),  # E6
        (3047, 100),  # C6
        (3319, 100),  # E6
        (4093, 200),  # C7
        (4093, 200),  # C7

    ]

    for note in pixhawk_melody:
            freq, duration = note
            send_value_to_arduino(6, f"{freq},{duration}",master)



def arm(master):
    for f in range(10):
        buzzer_play(master)
    for i in range(6):
        send_value_to_arduino(i, 0,master)
    print("ESC arming...")
    time.sleep(5)  # ESC'leri arm etmek için bekle
    print("sifirlanıyor")
    sifirla()
    time.sleep(2)



def ileri_geri(value):
    send_value_to_arduino(0, value)  # Motor 1 düz
    send_value_to_arduino(1, value)  # Motor 2 düz
    send_value_to_arduino(2, value)  # Motor 3 ters
    send_value_to_arduino(3, value)  # Motor 4 ters

def bat_cik(value):
    send_value_to_arduino(4, value)  # Motor 5 düz
    send_value_to_arduino(5, value)  # Motor 6 düz

def yanla(value):
    send_value_to_arduino(0, value)     # Motor 1 düz
    send_value_to_arduino(2, 170-value)     # Motor 3 düz
    send_value_to_arduino(1, 170-value) # Motor 2 ters
    send_value_to_arduino(3, value) # Motor 4 ters

def sag_sol(value):
    send_value_to_arduino(1, 170-value)     # Motor 2 düz
    send_value_to_arduino(3, 170-value) # Motor 4 ters
    send_value_to_arduino(2, value)     # Motor 3 düz
    send_value_to_arduino(0, value) # Motor 1 ters


def roll(value):
	send_value_to_arduino(4,value)
	send_value_to_arduino(5,179-value)




def ates():
	send_value_to_arduino(7, 180)

def kilitle():
	send_value_to_arduino(7,15)

def lidar(d):
	dosya=open("/home/rasp/atilay/lidx","r")
	x=dosya.read()
	dosya.close()

	dosya=open("/home/rasp/atilay/lidy0","r")
	y0=dosya.read()
	dosya.close()

	dosya=open("/home/rasp/atilay/lidy1","r")
	y1=dosya.read()
	dosya.close()

	dosya=open("/home/rasp/atilay/lidz","r")
	z=dosya.read()
	dosya.close()
	

	if d == "x":
		try:
			int(x)
			return x
		except:
			return 0
	elif d == "y0":
		try:
			int(y0)
			return y0
		except:
			return 0

	elif d == "y1":
		try:
			int(y1)
			return y1
		except:
			return 0
	elif d == "z":
		try:
			int(z)
			return z
		except:
			return 0

def piksel(d):
	dosya=open("/home/rasp/atilay/x","r")
	x=dosya.read()
	dosya.close()

	dosya=open("/home/rasp/atilay/y","r")
	y=dosya.read()
	dosya.close()


	if d == "x":
		try:
			int(x)
			return x
		except:
			return 0

	elif d == "y":

		try:
			int(y)
			return y
		except:
			return 0



def yanla(value=87,master=set()):

    send_value_to_arduino(0, 179-value,master)     # Motor 1 düz
    send_value_to_arduino(2, 179-value,master)     # Motor 3 düz
    send_value_to_arduino(1, value,master) # Motor 2 ters
    send_value_to_arduino(3, value,master) # Motor 4 ters



def sifirla(master=set()):
        send_value_to_arduino(0,86,master )  
        send_value_to_arduino(1,86,master)  
        send_value_to_arduino(2,87,master) 
        send_value_to_arduino(3, 88,master)  
        send_value_to_arduino(4, 88,master)  
        send_value_to_arduino(5,87)
"""

def don(master,gorev=False):
        kontrol=0

        ilk_derece=atilay.pusula(master)
        a=0
        while True:
                atilay.ileri_geri(1480,master)

                son_derece=atilay.pusula(master)
                son_fark=abs(son_derece-ilk_derece)
                print(abs(son_derece-ilk_derece))

                if abs(son_fark>=90) or gorev:
                        ilk_derece=atilay.pusula(master)
                        kontrol+=1
                        if kontrol>=4 or gorev:
                                while True:
                                        atilay.ileri_geri(1480,master)
                                return gorev
"""


def derinlik(x=50):
	dosya=open("/home/rasp/atilay/derinlik","w")
	dosya.write(str(x))
	dosya.close()
