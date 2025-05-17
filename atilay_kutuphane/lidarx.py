# -*- coding: utf-8 -*
import time
import serial
# written by Ibrahim for Public use

# Checked with TFmini plus

# ser = serial.Serial("/dev/ttyUSB1", 115200)

x = serial.Serial("/dev/ttyAMA"+str(0), 115200)






def read_data_x():
    
    while True:
        time.sleep(0.08)
        counter = x.in_waiting # count the number of bytes of the serial po>
        if counter > 8:
            bytes_serial = x.read(9)
            x.reset_input_buffer()

            if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59: # this >
                #print("Printing python3 portion")            
                distance = bytes_serial[2] + bytes_serial[3]*256 # multipli>
                strength = bytes_serial[4] + bytes_serial[5]*256
                temperature = bytes_serial[6] + bytes_serial[7]*256
                temperature = (temperature/8) - 256
                #print("Distance:"+ str(distance))
                #print("Strength:" + str(strength))
                #if temperature != 0:
                    #print("Temperature:" + str(temperature))
                x.reset_input_buffer()

                print(distance)
                dosya=open("/home/rasp/atilay/lidx","w")
                dosya.write(str(int(distance)))
                dosya.close()
                return distance






while True:
    if __name__ == "__main__":
        try:

            if x.isOpen() == False:
                x.open()
            read_data_x()

        except: # ctrl + c in terminal.

            if x != None:
                x.close()
