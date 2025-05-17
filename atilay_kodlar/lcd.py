import time
import digitalio
import board
import adafruit_character_lcd.character_lcd as character_lcd

# LCD'nin boyutları (16x2)
lcd_columns = 16
lcd_rows = 2

# Raspberry Pi pinleri
lcd_rs = digitalio.DigitalInOut(board.D25)
lcd_en = digitalio.DigitalInOut(board.D24)
lcd_d4 = digitalio.DigitalInOut(board.D23)
lcd_d5 = digitalio.DigitalInOut(board.D17)
lcd_d6 = digitalio.DigitalInOut(board.D18)
lcd_d7 = digitalio.DigitalInOut(board.D22)

# LCD objesi oluştur
lcd = character_lcd.Character_LCD_Mono(
    lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows
)

# Ekranı temizle
lcd.clear()

# Ekrana yazı yaz
lcd.message = "Merhaba, Dunya!"

# 5 saniye bekle
time.sleep(5)

# Ekranı temizle
lcd.clear()
