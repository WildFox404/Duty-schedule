import os
import cv2

image_path = './zhangsan.png'

if os.path.exists(image_path) and os.path.isfile(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error reading image: {image_path}")
    else:
        pass
# 处理图像...
else:
    print(f"File not found or not a file: {image_path}")