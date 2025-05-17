import serial
import time

# Arduino'nun bağlı olduğu seri portun doğru olduğunu kontrol edin
ser = serial.Serial('/dev/ttyACM0', 9600)  # '/dev/ttyACM0' yerine doğru portu kullanın

def send_value_to_arduino(motor_num, value):
    command = f"{motor_num},{value}\n"
    ser.write(command.encode())  # Komutu Arduino'ya gönder
    time.sleep(0.1)  # Biraz bekle, böylece Arduino veriyi işleyebilir

def arm_motors():
    for i in range(6):
        send_value_to_arduino(i, 0)
    print("ESC arming...")
    time.sleep(5)  # ESC'leri arm etmek için bekle

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


def rol(value):
	send_value_to_arduino(4,value)
	send_value_to_arduino(5,179-value)
# Test fonksiyonları
try:
    arm_motors()  # ESC'leri arm et
    while True:
            yanla(170)
            time.sleep(5)
except KeyboardInterrupt:
    print("Program sonlandırılıyor.")
finally:
    ser.close()  # Seri portu kapat
