import os
from PIL import Image

def resimleri_jpg_ye_donustur(klasor_yolu):
    """
    Belirtilen klasördeki tüm resimleri JPG formatına dönüştürür.

    Args:
        klasor_yolu: Tarayılacak klasörün yolu.
    """

    for dosya_adi in os.listdir(klasor_yolu):
        dosya_yolu = os.path.join(klasor_yolu, dosya_adi)
        if os.path.isfile(dosya_yolu) and not dosya_adi.endswith(".jpg"):
            try:
                # Görüntüyü aç
                img = Image.open(dosya_yolu)

                # JPG olarak kaydet
                yeni_dosya_yolu = os.path.splitext(dosya_yolu)[0] + ".jpg"
                img.save(yeni_dosya_yolu, "JPEG")

                # Orijinal dosyayı sil (isteğe bağlı)
                # os.remove(dosya_yolu)

                print(f"{dosya_adi} JPG formatına dönüştürüldü.")

            except Exception as e:
                print(f"{dosya_adi} dönüştürülemedi: {e}")

# Klasör Yolları
klasorler = ["dataset/test/images", "dataset/validation/images", "dataset/train/images"]

# Resimleri JPG'ye Dönüştür
for klasor in klasorler:
    resimleri_jpg_ye_donustur(klasor)

print("Tüm resimler JPG formatına dönüştürüldü!")
