import cv2
from picamera2 import Picamera2

picam2 = Picamera2()

def capture_image():
    """
    Captura uma imagem com a câmera e retorna o caminho do arquivo.
    
    Returns:
        str: Caminho da imagem capturada.
    """
    picam2.start()
    image_path = "test.jpg"
    picam2.capture_file(image_path)
    print(f"Imagem capturada: {image_path}")
    return image_path