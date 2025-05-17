# -*- coding: utf-8 -*
import time
import serial
# written by Ibrahim for Public use

# Checked with TFmini plus

# ser = serial.Serial("/dev/ttyUSB1", 115200)

z = serial.Serial("/dev/ttyAMA"+str(3), 115200)






def read_data_z():
    
    while True:
        time.sleep(0.08)
        counter = z.in_waiting # count the number of bytes of the serial po>
        if counter > 8:
            bytes_serial = z.read(9)
            z.reset_input_buffer()

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
                z.reset_input_buffer()

                print(distance)
                dosya=open("/home/rasp/atilay/lidz","w")
                dosya.write(str(int(distance)))
                dosya.close()
                return distance







if __name__ == "__main__":
        try:

            if z.isOpen() == False:
                z.open()
            read_data_z()

        except: # ctrl + c in terminal.

            if z != None:
                z.close()
