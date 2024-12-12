#define RX_PIN 16
#define TX_PIN 17
HardwareSerial UART(2);

void setup() {
  Serial.begin(115200);
  UART.begin(9600, SERIAL_8N1, RX_PIN, TX_PIN);
  Serial.println("ESP32 UART Teste Iniciado!");
}

void loop() {
  // Envia mensagem para a Raspberry Pi
  String mensagem = "ESP32 -> Raspberry Pi\n";
  UART.print(mensagem);
  Serial.println("Mensagem enviada: " + mensagem);

  // Aguarda e processa mensagens recebidas
  while (UART.available()) {
    String recebido = UART.readStringUntil('\n');
    Serial.println("Recebido: " + recebido);
  }

  delay(1000);
}
