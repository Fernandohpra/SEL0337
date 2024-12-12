from ultralytics import YOLO

# Carregar o modelo YOLO
ncnn_model = YOLO("yolo11n_ncnn_model")

def detect_objects(image_path):
    """
    Detecta objetos em uma imagem e retorna uma lista de categorias detectadas.
    
    Args:
        image_path (str): Caminho da imagem a ser processada.
        
    Returns:
        list: Lista de categorias de objetos detectados.
    """
    results = ncnn_model(image_path)  # Faz a predição na imagem
    categories = []

    # Extraímos os nomes das categorias dos objetos detectados
    for result in results:
        for cls in result.boxes.cls:
            categories.append(result.names[int(cls)])

    # Remover duplicatas
    unique_categories = list(set(categories))
    print(f"Objetos detectados: {unique_categories}")
    return unique_categories