import time
import board
import busio
import adafruit_bmp3xx

# I2C bağlantısını başlatın
i2c = busio.I2C(board.SCL, board.SDA)

# Sensörün adresini seçin (0x76 veya 0x68)
# Hangi adresin sensörünüze ait olduğunu i2cdetect ile kontrol edin
sensor_address = 0x76  # Sensörünüz 0x76 adresinde ise

# BMP3xx sensörünü başlatın
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c, address=sensor_address)

# Deniz seviyesi basıncını ayarlayın (gerekirse)
bmp.sea_level_pressure = 1013.25  # Standart deniz seviyesi basıncı

while True:
    # Basınç ve Sıcaklık
    pressure = bmp.pressure
    temperature = bmp.temperature

    # Yükseklik
    altitude = bmp.altitude-1053

    # Tüm verileri ekrana yazdırın
    print(f"Basınç: {pressure:.2f} hPa")
    print(f"Sıcaklık: {temperature:.2f} °C")
    print(f"Yükseklik: {altitude:.2f} m")

    # 1 saniye bekleyin
    time.sleep(1)
