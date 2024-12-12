import serial
import time
from camera import capture_image
from yolo import detect_objects

# Configuração do UART
uart = serial.Serial(port="/dev/serial0", baudrate=115200, timeout=1)

# Limpa o buffer inicial
uart.reset_input_buffer()
print("Raspberry Pi UART Teste Iniciado!")

try:
    while True:
        # Recebe a flag da ESP32
        if uart.in_waiting > 0:
            flag = uart.readline().decode("utf-8", errors="ignore").strip()
            print(f"Flag recebida: {flag}")
            
            if flag == "1":
                print("Capturando imagem...")
                image_path = capture_image()  # Captura a imagem com a câmera
                
                print("Detectando objetos...")
                objects = detect_objects(image_path)  # Detecta objetos com o YOLO

                # Envia resultado para ESP32
                if objects:
                    message = "|".join(objects)
                else:
                    message = "Nothing"  # Nenhum objeto detectado
                
                uart.write((message + "\n").encode("utf-8"))
                print(f"Enviado para ESP32: {message}")

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Encerrando programa...")
finally:
    uart.close()
