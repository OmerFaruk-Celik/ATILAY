import RPi.GPIO as GPIO
import time
import subprocess

# Lidar PWM pini ve kontrol pini
LIDAR_PWM_PIN = 12  # GPIO 18, Pin 12
LIDAR_CONTROL_PIN = 23  # GPIO 23
#LIDAR_PWM_PIN = 13  # GPIO 18, Pin 12
#LIDAR_CONTROL_PIN = 24  # GPIO 23


# GPIO ayarları
GPIO.setwarnings(False)  # Uyarıları devre dışı bırak
GPIO.setmode(GPIO.BCM)
GPIO.setup(LIDAR_PWM_PIN, GPIO.IN)
GPIO.setup(LIDAR_CONTROL_PIN, GPIO.OUT, initial=GPIO.LOW)

# Sıcaklık düzeltme faktörü
TEMPERATURE_COMPENSATION_FACTOR = 0.025  # Her bir derece için 0.015 cm düzeltme

def get_cpu_temperature():
    # Komut satırından CPU sıcaklığını al
    temp_output = subprocess.run(["vcgencmd", "measure_temp"], capture_output=True, text=True)
    temp_str = temp_output.stdout
    # Çıktıdan sıcaklık değerini ayıkla
    temp_value = float(temp_str.split('=')[1].split("'")[0])
    return temp_value

def read_distance():
    GPIO.output(LIDAR_CONTROL_PIN, GPIO.LOW)
    # PWM sinyali düşük olduğunda bekle
    while GPIO.input(LIDAR_PWM_PIN) == GPIO.LOW:
        pass

    # PWM sinyali yüksek olduğunda zamanlamayı başlat
    start_time = time.perf_counter()

    # PWM sinyali tekrar düşük olduğunda zamanı ölç
    while GPIO.input(LIDAR_PWM_PIN) == GPIO.HIGH:
        pass
    end_time = time.perf_counter()

    GPIO.output(LIDAR_CONTROL_PIN, GPIO.HIGH)

    # Zaman farkını ölç ve mesafeyi hesapla
    pulse_duration = end_time - start_time
    distance = pulse_duration * 100000  # cm cinsinden mesafe

    # Raspberry Pi'nin işlemci sıcaklığını al
    current_temperature = get_cpu_temperature()

    # Sıcaklık düzeltmesi uygula
    distance += (current_temperature - 20) * TEMPERATURE_COMPENSATION_FACTOR

    return distance

try:
    while True:
        distance = int(read_distance())
        print(f"Mesafe: {distance} cm")
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Program durduruldu.")
finally:
    GPIO.cleanup()
