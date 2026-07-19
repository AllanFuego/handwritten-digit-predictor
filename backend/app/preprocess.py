import cv2
import numpy as np


def preprocess_image(image_bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

    if img is None:
        raise ValueError("Could not read image")

    img = cv2.resize(img, (28, 28))

    if np.mean(img) > 127:
        img = 255 - img

    img = img.astype(np.float32) / 255.0

    return img.flatten().reshape(1, -1)