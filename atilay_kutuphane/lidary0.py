# -*- coding: utf-8 -*
import time
import serial
# written by Ibrahim for Public use

# Checked with TFmini plus

# ser = serial.Serial("/dev/ttyUSB1", 115200)

y0 = serial.Serial("/dev/ttyAMA"+str(1), 115200)






def read_data_y0():
    
    while True:
        time.sleep(0.08)
        counter = y0.in_waiting # count the number of bytes of the serial po>
        if counter > 8:
            bytes_serial = y0.read(9)
            y0.reset_input_buffer()

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
                y0.reset_input_buffer()

                print(distance)
                dosya=open("/home/rasp/atilay/lidy0","w")
                dosya.write(str(int(distance)))
                dosya.close()
                return distance







if __name__ == "__main__":
        try:

            if y0.isOpen() == False:
                y0.open()
            read_data_y0()

        except: # ctrl + c in terminal.

            if y0 != None:
                y0.close()
