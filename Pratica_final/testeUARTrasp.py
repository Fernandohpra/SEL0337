import serial
import time

uart = serial.Serial(port='/dev/serial0', baudrate=9600, timeout=1)

# Limpa o buffer no início
uart.reset_input_buffer()
print("Raspberry Pi UART Teste Iniciado!")

try:
    while True:
        # Recebe mensagem da ESP32
        if uart.in_waiting > 0:
            mensagem_recebida = uart.readline().decode('utf-8', errors='ignore').strip()
            print(f"Recebido: {mensagem_recebida}")
        
        # Envia mensagem para ESP32
        mensagem_envio = "Raspberry Pi -> ESP32\n"
        uart.write(mensagem_envio.encode('utf-8'))
        print(f"Enviado para ESP32: {mensagem_envio.strip()}")

        time.sleep(1)

except KeyboardInterrupt:
    print("Encerrando comunicação UART...")
    uart.close()