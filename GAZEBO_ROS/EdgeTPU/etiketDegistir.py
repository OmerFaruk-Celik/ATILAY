import os
import xml.etree.ElementTree as ET

def etiketleri_degistir(klasor_yolu):
    annotations_klasoru = os.path.join(klasor_yolu, "annotations")
    for dosya_adi in os.listdir(annotations_klasoru):
        if dosya_adi.endswith(".xml"):
            dosya_yolu = os.path.join(annotations_klasoru, dosya_adi)
            tree = ET.parse(dosya_yolu)
            root = tree.getroot()

            for obj in root.findall('object'):
                name_tag = obj.find('name')
                name_tag.text = "daire"  # Etiketi "cember" olarak değiştir

            tree.write(dosya_yolu)

# Klasör Yolları
klasorler = ["dataset/test", "dataset/validation", "dataset/train"]

# Etiketleri Değiştir
for klasor in klasorler:
    etiketleri_degistir(klasor)

print("Etiketler başarıyla değiştirildi!")
