import serial
import time

# Arduino'nun bağlı olduğu seri portun doğru olduğunu kontrol edin
ser = serial.Serial('/dev/ttyACM0', 9600)  # '/dev/ttyACM0' yerine doğru portu >

def send_value_to_arduino(motor_num, value):
    command = f"{motor_num},{value}\n"
    ser.write(command.encode())  # Komutu Arduino'ya gönder
    time.sleep(0.1)  # Biraz bekle, böylece Arduino veriyi işleyebilir

while True:
	value=int(input("derece:"))
	send_value_to_arduino(7,value)

