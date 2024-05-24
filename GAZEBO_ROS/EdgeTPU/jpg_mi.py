import os

def olmayan_jpg_resimleri_bul(klasor_yolu):
    """
    Belirtilen klasördeki JPG formatında olmayan resimleri bulur.

    Args:
        klasor_yolu: Tarayılacak klasörün yolu.

    Returns:
        JPG formatında olmayan resim dosyalarının bir listesi.
    """

    olmayan_jpg_resimler = []
    for dosya_adi in os.listdir(klasor_yolu):
        if not dosya_adi.endswith(".jpg") and dosya_adi.lower().endswith((".png", ".bmp", ".gif")):  # JPG olmayan ve diğer resim formatları için kontrol
            dosya_yolu = os.path.join(klasor_yolu, dosya_adi)
            olmayan_jpg_resimler.append(dosya_yolu)

    return olmayan_jpg_resimler

# Klasör Yolları
klasorler = ["dataset/test", "dataset/validation", "dataset/train"]

# JPG olmayan resimleri bul ve ekrana yazdır
for klasor in klasorler:
    olmayan_jpg_resimler = olmayan_jpg_resimleri_bul(klasor)
    if olmayan_jpg_resimler:
        print(f"{klasor} klasöründe bulunan JPG olmayan resimler:")
        for resim in olmayan_jpg_resimler:
            print(resim)
    else:
        print(f"{klasor} klasöründe JPG olmayan resim bulunamadı.")

print("İşlem tamamlandı!")
