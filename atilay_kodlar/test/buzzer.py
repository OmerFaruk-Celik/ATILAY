import serial
import time

# Arduino'nun bağlı olduğu seri portu doğru şekilde ayarlayın
ser = serial.Serial('/dev/ttyACM0', 9600)  # '/dev/ttyACM0' yerine doğru portu kullanın

def send_value_to_arduino(motor_num, value):
    command = f"{motor_num},{value}\n"
    ser.write(command.encode())  # Komutu Arduino'ya gönder
    time.sleep(0.01)  # Biraz bekle, böylece Arduino veriyi işleyebilir

def buzzer_play(freq, duration):
    send_value_to_arduino(6, f"{freq},{duration}")

# Pixhawk arming melodisi için frekans ve süre bilgileri
pixhawk_melody = [
    (3047, 100),  # C6
    (3319, 100),  # E6
    (3568, 100),  # G6
    (3047, 100),  # C6
    (3319, 100),  # E6
    (3568, 100),  # G6
    (3047, 100),  # C6
    (3319, 100),  # E6
    (3568, 100),  # G6

    (4093, 200),  # C7
    (4093, 200),  # C7
    (4093, 200),  # C7
    (4093, 200),  # C7
    (4093, 200),  # C7
    (4093, 200),  # C7
    (4093, 200),  # C7
    (4093, 200),  # C7
    (4093, 200),  # C7
    (3093, 200),  # C7
    (3093, 200),  # C7
    (4093, 200),  # C7
    (4093, 200),  # C7
    (3093, 200),  # C7
    (3093, 200),  # C7
    (3093, 200),  # C7


]
try:
    for i in range(1):
        for note in pixhawk_melody:
            freq, duration = note
            buzzer_play(freq, duration)
            time.sleep(duration / 1000.0)  # Notalar arasındaki süre
except KeyboardInterrupt:
    print("Program sonlandırılıyor.")
finally:
    ser.close()  # Seri portu kapat
