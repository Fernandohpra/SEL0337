// Definição de pinos
#define LDR_PIN 34  // Pino ADC conectado ao divisor de tensão do LDR

// Variáveis
int leituraADC = 0;  // Variável para armazenar a leitura do ADC
float tensao = 0.0;  // Variável para armazenar a tensão correspondente

void setup() {
  Serial.begin(115200);  // Inicializa a comunicação serial
}

void loop() {
  // Leitura do ADC
  leituraADC = analogRead(LDR_PIN);
  
  // Conversão para tensão (faixa de 0 a 3.3V)
  tensao = leituraADC * (3.3 / 4095.0);

  // Exibe os valores no monitor serial
  Serial.print("Leitura do ADC: ");
  Serial.print(leituraADC);
  Serial.print(" -> Tensão: ");
  Serial.print(tensao, 2);
  Serial.println(" V");

  // Delay para estabilidade de leitura
  delay(500);
}

