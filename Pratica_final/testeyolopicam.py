from picamera2 import Picamera2
from ultralytics import YOLO

# Inicializa a câmera
camera = Picamera2()
camera.configure(camera.create_still_configuration())

# Modelo YOLO
model = YOLO("yolo11x.pt")  # Substitua pelo caminho do seu modelo

def capture_photo(photo_path="test_image.jpg"):
    """
    Captura uma foto e salva no caminho especificado.
    """
    camera.start()
    camera.capture_file(photo_path)
    camera.stop()
    print(f"Foto capturada: {photo_path}")
    return photo_path

def detect_objects(photo_path):
    """
    Detecta objetos em uma foto usando YOLO.

    Args:
        photo_path (str): Caminho da foto capturada.

    Returns:
        list: Lista de categorias detectadas.
    """
    results = model(photo_path)  # Inferência
    categories = []
    for result in results:
        for cls in result.boxes.cls:
            categories.append(result.names[int(cls)])
    unique_categories = list(set(categories))
    return unique_categories

if __name__ == "__main__":
    print("Capturando foto para teste...")
    photo_path = capture_photo()

    print("Detectando objetos...")
    detected_objects = detect_objects(photo_path)
    
    print("Objetos detectados:")
    for obj in detected_objects:
        print(f"- {obj}")
