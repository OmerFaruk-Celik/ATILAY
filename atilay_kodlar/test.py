import time

def uzun_dongu():
  """Uzun süren bir döngü örneği."""
  for i in range(10):
    time.sleep(0.5)
    # Bir şey yap, örneğin bir işlem veya hesaplama
    pass

# Başlangıç zamanını kaydet
baslangic_zamani = time.time()

# Döngüyü çalıştır
uzun_dongu()

# Bitiş zamanını kaydet
bitis_zamani = time.time()

# Geçen süreyi hesapla
gecen_sure = bitis_zamani - baslangic_zamani

# Sonucu yazdır
print(f"Döngü {gecen_sure:.4f} saniye sürdü.")
