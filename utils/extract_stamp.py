import cv2
import os
import numpy as np
from .ocr import extract_text

def detect_stamps(image_path, output_folder):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                                   cv2.THRESH_BINARY_INV, 11, 3)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    results = []
    for i, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        if 1000 < area < 100000:
            x, y, w, h = cv2.boundingRect(cnt)
            roi = img[y:y+h, x:x+w]
            stamp_file = f"stamp_{i}.png"
            full_path = os.path.join(output_folder, stamp_file)
            cv2.imwrite(full_path, roi)
            text = extract_text(roi).strip()
            results.append({'image': stamp_file, 'text': text})
    return results
