import cv2
import numpy as np
import matplotlib.pyplot as plt


def preprocess_image(image):
    """Gürültü azaltma ve histogram eşitleme uygular."""
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    equalized = cv2.equalizeHist(blurred)
    return equalized

def threshold_image(image):
    """Beyin dokusunu ayırmak için görüntüyü eşikler."""
    _, thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

def find_brain_contour(thresh_image):
    """Beynin konturunu bulur."""
    contours, _ = cv2.findContours(thresh_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    brain_contour = max(contours, key=cv2.contourArea)
    return brain_contour

def calculate_brain_area(contour):
    """Beynin alanını hesaplar (mm² cinsinden)."""
    area_in_pixels = cv2.contourArea(contour)
    return area_in_pixels



def getArea(image):
    # 2. Ön İşleme
    try:
        preprocessed_image = preprocess_image(image)

        # 3. Eşikleme
        thresh_image = threshold_image(preprocessed_image)

        # 4. Beyin Konturunu Bulma
        brain_contour = find_brain_contour(thresh_image)

        # 5. Alan Hesaplama
        brain_area_mm2 = calculate_brain_area(brain_contour)
        return brain_area_mm2
    except:
        return 0
