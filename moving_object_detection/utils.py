import cv2
import numpy as np

def threshold_image(image: np.array) -> np.array:
        blur = blur_image(image)
        _, ret = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return ret

def blur_image(image: np.array) -> np.array:
    blur = cv2.GaussianBlur(image, (5, 5), 0)
    return blur