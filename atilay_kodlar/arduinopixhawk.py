import serial
import time

# Arduino'nun bağlı olduğu seri portun doğru olduğunu kontrol edin
ser = serial.Serial('/dev/ttyACM0', 9600)  # '/dev/ttyUSB0' yerine doğru portu kullanın

def send_value_to_arduino(motor_num, value):
    command = f"{motor_num},{value}\n"
    ser.write(command.encode())  # Komutu Arduino'ya gönder
    time.sleep(0.1)  # Biraz bekle, böylece Arduino veriyi işleyebilir

try:
    # ESC'yi arm etmek için her motor için minimum sinyali gönderin
    for motor_num in range(6):
        send_value_to_arduino(motor_num, 0)
    print("ESC arming...")
    time.sleep(5)  # 5 saniye bekle

    while True:
        for motor_num in range(6):  # 6 motor için
            for value in range(0, 180, 5):  # 70'den 110'a kadar 1'er adımlarla
                send_value_to_arduino(motor_num, value)
                print(f"Sent to motor {motor_num}: {value}")
                time.sleep(0.01)  # 0.02 saniye bekle
            for value in range(180, 0, -5):  # 110'dan 70'e kadar 1'er adımlarla geri
                send_value_to_arduino(motor_num, value)
                print(f"Sent to motor {motor_num}: {value}")
                time.sleep(0.01)  # 0.02 saniye bekle
except KeyboardInterrupt:
    print("Program sonlandırılıyor.")
finally:
    ser.close()  # Seri portu kapat
