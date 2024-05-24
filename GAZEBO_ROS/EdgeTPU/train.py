import numpy as np
import os

from tflite_model_maker.config import ExportFormat
from tflite_model_maker import model_spec
from tflite_model_maker import object_detector

import tensorflow as tf
assert tf.__version__.startswith('2')

tf.get_logger().setLevel('ERROR')
from absl import logging
logging.set_verbosity(logging.ERROR)

# Veri Seti Parametreleri
use_custom_dataset = True  # Özel veri seti kullanılıyorsa True olarak ayarlayın
dataset_is_split = True   # Veri seti zaten bölünmüşse True olarak ayarlayın

# Özel Veri Seti Bilgileri (use_custom_dataset = True ise)
if use_custom_dataset:
  # ZIP dosyasının yolu (eğer ZIP kullanılıyorsa)
  dataset_zip_path = "dataset.zip"

  # Etiketler sözlüğü
  label_map = {1: "cember",2: "dikdortgen",3: "daire",4: "ucgen",5: "kare",6: "insan",7: "yazi"}

  # Veri seti yolları
  if dataset_is_split:
    train_images_dir = "dataset/train/images"
    train_annotations_dir = "dataset/train/annotations"
    val_images_dir = "dataset/validation/images"
    val_annotations_dir = "dataset/validation/annotations"
    test_images_dir = "dataset/test/images"
    test_annotations_dir = "dataset/test/annotations"
  else:
    images_dir = "dataset/images"
    annotations_dir = "dataset/annotations"

# Model Parametreleri
model_spec = object_detector.EfficientDetLite0Spec()  # Model seçimi
epochs = 5              # Eğitim dönemi sayısı
batch_size = 10           # Batch boyutu
train_whole_model = True  # Tüm modeli eğitmek için True

# Edge TPU Parametreleri
use_edge_tpu = True    # Edge TPU kullanılıyorsa True olarak ayarlayın
NUMBER_OF_TPUS = 1     # Kullanılacak Edge TPU sayısı

# Çıktı Dosyaları
TFLITE_FILENAME = "efficientdet-lite-salad.tflite"
LABELS_FILENAME = "salad-labels.txt"

# Model Kaydetme Dizini
model_dir = "./models"
if not os.path.exists(model_dir):
  os.makedirs(model_dir)
  
  
# Veri Setini Yükleme
if use_custom_dataset:
    if dataset_is_split:
      train_data = object_detector.DataLoader.from_pascal_voc(train_images_dir, train_annotations_dir, label_map=label_map)
      validation_data = object_detector.DataLoader.from_pascal_voc(val_images_dir, val_annotations_dir, label_map=label_map)
      test_data = object_detector.DataLoader.from_pascal_voc(test_images_dir, test_annotations_dir, label_map=label_map)
    else:
      print("not use custom dataset")		
    # Veri setini bölme (gerekirse)
    # ...

# Model Oluşturma ve Eğitme
model = object_detector.create(train_data, model_spec, validation_data, epochs, batch_size, train_whole_model=train_whole_model)
#model.export_saved_model(model_dir)


# Modeli Değerlendirme
model.evaluate(test_data)

# TensorFlow Lite'a Dönüştürme
model.export(export_dir=".", tflite_filename=TFLITE_FILENAME, label_filename=LABELS_FILENAME, export_format=[ExportFormat.TFLITE, ExportFormat.LABEL])

# Dönüştürülen Modeli Değerlendirme
model.evaluate_tflite(TFLITE_FILENAME, test_data)

# Edge TPU için Derleme (İsteğe Bağlı)
if use_edge_tpu:
  print("edge_tpu aktif et")
  # Edge TPU derleyicisini kullanarak modeli derleme
  #!edgetpu_compiler $TFLITE_FILENAME -d --num_segments=$NUMBER_OF_TPUS
  print("install edgetpu compiler")
# ... (Edge TPU'da çalıştırma örneği - isteğe bağlı)
