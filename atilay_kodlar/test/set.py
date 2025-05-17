from pymavlink import mavutil
import time

# Pixhawk'a bağlan
master = mavutil.mavlink_connection('/dev/ttyACM0', baud=115200)

# Heartbeat bekle
master.wait_heartbeat()

# ARM komutunu gönder
def arm_vehicle():
    master.arducopter_arm()
    master.motors_armed_wait()
    print("Vehicle armed!")

# DISARM komutunu gönder
def disarm_vehicle():
    master.arducopter_disarm()
    master.motors_disarmed_wait()
    print("Vehicle disarmed!")

# PWM değerlerini gönderme fonksiyonu
def set_servo_pwm(servo_n, pwm_value):
    master.set_servo(servo_n, pwm_value)

# ESC kalibrasyonu
def calibrate_esc():
    # Max PWM değeri gönder
    max_pwm = 1800
    print("Sending max PWM")
    for i in range(1, 5):  # 1'den 4'e kadar olan kanallar
        set_servo_pwm(i, max_pwm)
    time.sleep(2)  # 2 saniye bekle

    # Min PWM değeri gönder
    min_pwm = 1200
    print("Sending min PWM")
    for i in range(1, 5):  # 1'den 4'e kadar olan kanallar
        set_servo_pwm(i, min_pwm)
    time.sleep(2)  # 2 saniye bekle

    print("ESC Calibration complete")

# Motorları çalıştırma
def start_motors():
    run_pwm = 1500  # Motorları çalıştırmak için ortalama PWM değeri
    print("Starting motors")
    for i in range(1, 5):  # 1'den 4'e kadar olan kanallar
        set_servo_pwm(i, run_pwm)
    time.sleep(5)  # Motorları 5 saniye çalıştır
    print("Motors running")

# Aracın arm durumu kontrol et ve arm et
if not master.motors_armed():
    arm_vehicle()
    time.sleep(2)  # 2 saniye bekle

# ESC kalibrasyonunu başlat
calibrate_esc()

# Motorları çalıştır
start_motors()

# Aracı disarm et
disarm_vehicle()
