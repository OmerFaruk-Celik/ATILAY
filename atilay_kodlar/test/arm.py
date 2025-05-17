import serial
import time

# Arduino'nun bağlı olduğu seri portun doğru olduğunu kontrol edin
ser = serial.Serial('/dev/ttyACM0', 9600)  # '/dev/ttyUSB0' yerine doğru portu kullanın

def send_value_to_arduino(motor_num, value):
    command = f"{motor_num},{value}\n"
    ser.write(command.encode())  # Komutu Arduino'ya gönder
    time.sleep(0.1)  # Biraz bekle, böylece Arduino veriyi işleyebilir

try:
    print("ESC kalibrasyonuna başlanıyor...")

    # Maksimum sinyali gönder
    print("Maksimum sinyal gönderiliyor...")
    for motor_num in range(6):
        send_value_to_arduino(motor_num, 180)
    time.sleep(2)  # 2 saniye bekle

    # Minimum sinyali gönder
    print("Minimum sinyal gönderiliyor...")
    for motor_num in range(6):
        send_value_to_arduino(motor_num, 0)
    time.sleep(2)  # 2 saniye bekle

    print("Kalibrasyon tamamlandı.")
except KeyboardInterrupt:
    print("Program sonlandırılıyor.")
finally:
    ser.close()  # Seri portu kapat
