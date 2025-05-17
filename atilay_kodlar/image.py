import cv2

# Kamera açma
cap = cv2.VideoCapture(0)

# Kamera açılmasını kontrol et
if not cap.isOpened():
    print("Kamera açılamadı!")
    exit()

# Çerçeve okuma
ret, frame = cap.read()

# Çerçeve okunup okunmadığını kontrol et
if not ret:
    print("Görüntü alınamadı!")
else:
    # Görüntüyü kaydet
    cv2.imwrite('image.png', frame)
    print("Görüntü kaydedildi.")

# Kaynağı serbest bırak
cap.release()

