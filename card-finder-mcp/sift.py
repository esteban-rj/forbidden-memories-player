#!/usr/bin/env python3
"""
SIFT Boolean - Función Mínima
============================

Función booleana mínima para detectar matches SIFT.
"""

import cv2 as cv
import numpy as np
import base64
from io import BytesIO

def has_sift_match(image_base64, template_base64, threshold=0.4, min_matches=4):
    """
    Retorna True si encuentra match, False si no.
    
    Args:
        image_base64 (str): Imagen en formato base64
        template_base64 (str): Plantilla en formato base64
        threshold (float): Umbral ratio test (0.0-1.0)
        min_matches (int): Mínimo de matches requeridos
    
    Returns:
        bool: True si hay match, False si no
    """
    try:
        # Decodificar imágenes base64
        img_data = base64.b64decode(image_base64)
        template_data = base64.b64decode(template_base64)
        
        # Convertir a arrays numpy
        img_array = np.frombuffer(img_data, dtype=np.uint8)
        template_array = np.frombuffer(template_data, dtype=np.uint8)
        
        # Decodificar imágenes
        img = cv.imdecode(img_array, cv.IMREAD_COLOR)
        template = cv.imdecode(template_array, cv.IMREAD_GRAYSCALE)
        
        if img is None or template is None:
            return False
        
        # Convertir a escala de grises
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        
        # SIFT
        sift = cv.SIFT_create()
        kp1, des1 = sift.detectAndCompute(img_gray, None)
        kp2, des2 = sift.detectAndCompute(template, None)
        
        if des1 is None or des2 is None:
            return False
        
        # Matching
        flann = cv.FlannBasedMatcher(
            dict(algorithm=1, trees=5), 
            dict(checks=50)
        )
        matches = flann.knnMatch(des2, des1, k=2)
        
        # Ratio test
        good_matches = [
            m for m, n in matches 
            if len(matches[0]) == 2 and m.distance < threshold * n.distance
        ]
        
        return len(good_matches) >= min_matches
        
    except:
        return False

def image_to_base64(image_path):
    """
    Convierte una imagen de archivo a base64.
    
    Args:
        image_path (str): Ruta de la imagen
    
    Returns:
        str: Imagen en formato base64
    """
    try:
        with open(image_path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except:
        return None

# Uso directo
if __name__ == "__main__":
    # Convertir imágenes a base64 para testing
    img_base64 = image_to_base64('template-test/InterfazJuego.png')
    template_base64 = image_to_base64('template-test/template_3.png')
    
    if img_base64 and template_base64:
        result = has_sift_match(img_base64, template_base64)
        print("✅ MATCH" if result else "❌ NO MATCH")
    else:
        print("❌ Error loading images") 