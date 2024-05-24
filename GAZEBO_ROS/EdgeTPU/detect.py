from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import tflite_runtime.interpreter as tflite
from pycoral.adapters import common
from pycoral.adapters import detect
from pycoral.utils.dataset import read_label_file
import cv2
import numpy as np

# Model ve Etiket Dosya Yolları
MODEL_PATH = "efficientdet-lite-salad.tflite"
LABELS_FILENAME = "salad-labels.txt"

# Etiketleri Yükle
labels = read_label_file(LABELS_FILENAME)

# Interpreter Oluştur
interpreter = tflite.Interpreter(MODEL_PATH)
interpreter.allocate_tensors()

# Giriş Tensör Bilgilerini Al
_, input_height, input_width, _ = interpreter.get_input_details()[0]['shape']

# Video Yakalama Başlat
#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('rosrecord5')
# Orijinal FPS değerini alın
original_fps = cap.get(cv2.CAP_PROP_FPS)
print("Orijinal FPS:", original_fps)

# Yeni FPS değerini hesaplayın (örneğin, 2 katı hız)
new_fps = 300#original_fps * 4

# FPS değerini ayarlayın
cap.set(cv2.CAP_PROP_FPS, new_fps)
sayac=0
while True:
    # Kare Yakala
    ret, frame = cap.read()

    # Görüntüyü PIL Image Formatına Dönüştür
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # Görüntüyü Yeniden Boyutlandır
    _, scale = common.set_resized_input(
        interpreter, image.size, lambda size: image.resize(size, Image.Resampling.LANCZOS))
    if sayac>=200:
        sayac=0		
        # Çıkarım Yap
        interpreter.invoke()
        objs = detect.get_objects(interpreter, score_threshold=0.7, image_scale=scale)

        # Tespiti Görüntüle
        draw = ImageDraw.Draw(image)
        for obj in objs:
            bbox = obj.bbox
            color = (0, 255, 0)  # Yeşil kutu
            draw.rectangle([(bbox.xmin, bbox.ymin), (bbox.xmax, bbox.ymax)], 
                           outline=color, width=3)
            draw.text((bbox.xmin + 4, bbox.ymin + 4),
                      '%s\n%.2f' % (labels.get(obj.id, obj.id), obj.score),
                      fill=color)

    # PIL Image'ı OpenCV Formatına Dönüştür
    sayac+=1
    result = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Görüntüyü Göster
    cv2.imshow("Nesne Tespiti", result)

    # Çıkış Tuşu
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kaynakları Serbest Bırak
cap.release()
cv2.destroyAllWindows()
