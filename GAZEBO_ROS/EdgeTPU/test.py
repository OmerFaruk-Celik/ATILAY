import random
import os
dataset_is_split=True
test_images_dir="./test"
# If you're using a custom dataset, we take a random image from the test set:
if True:
  images_path = test_images_dir if dataset_is_split else os.path.join(test_dir, "images")
  filenames = os.listdir(os.path.join(images_path))
  random_index = random.randint(0,len(filenames)-1)
  INPUT_IMAGE = os.path.join(images_path, filenames[random_index])
