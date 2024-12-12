#include <Wire.h>


#include <Adafruit_SSD1306.h>
#include <Adafruit_GFX.h>

// Configurações do display OLED
#define OLED_ADDRESS 0x3C  // Endereço I2C do display OLED
#define OLED_RESET -1      // Reset do display OLED (não utilizado)
Adafruit_SSD1306 display(128, 64, &Wire, OLED_RESET);

// Pinos da ESP32
#define TOUCH_PIN T0       // Pino touch (ajustar conforme necessário)
#define LDR_PIN 34         // Pino ADC conectado ao divisor de tensão do LDR

// Configuração da comunicação UART
HardwareSerial UART(1);

// Variáveis globais
int leituraADC = 0;             // Armazena a leitura do ADC do LDR
String resultFromRpi = "Nenhum objeto."; // Resultado inicial a ser exibido no display
bool waitingForResponse = false; // Estado de espera pela resposta da Raspberry Pi

// Mutex para proteger o acesso a variáveis compartilhadas
SemaphoreHandle_t mutex;

// Função para atualizar o display OLED
void updateDisplay(const String &status, const String &message) {
  xSemaphoreTake(mutex, portMAX_DELAY);  // Aguarda acesso ao display
  display.clearDisplay();

  // Exibe o status do sistema (luminosidade ou estado do sistema)
  display.setCursor(0, 0);
  display.setTextSize(1);
  display.println(status);

  // Exibe os objetos detectados na parte inferior
  display.setCursor(0, 20);
  display.setTextSize(1);
  display.println("Objetos detectados:");
  display.println(message);

  display.display();
  xSemaphoreGive(mutex);  // Libera o acesso ao display
}

// Task 1: Lê o LDR e atualiza o status do sistema (Core 0)
void taskLDR(void *pvParameters) {
  while (true) {
    leituraADC = analogRead(LDR_PIN);

    if (leituraADC < 1000) {
      // Luminosidade insuficiente
      updateDisplay("Luminosidade baixa,", "sistema desativado");
    } else {
      // Sistema ativo
      updateDisplay("Luminosidade OK", resultFromRpi);
    }

    vTaskDelay(pdMS_TO_TICKS(500));  // Atraso de 500ms
  }
}

// Task 2: Gerencia o botão touch, UART e atualiza o resultado (Core 1)
void taskTouchAndUART(void *pvParameters) {
  while (true) {
    if (leituraADC >= 1000) {  // Só prossegue se a luminosidade for suficiente
      // Verifica se o botão touch foi acionado
      if (!waitingForResponse && touchRead(TOUCH_PIN) < 40) {  // Ajustar o limiar do touch conforme necessário
        Serial.println("Botão touch acionado!");

        // Envia a flag para a Raspberry Pi
        UART.print("1\n");
        Serial.println("Flag enviada para a Raspberry Pi.");
        waitingForResponse = true;  // Define estado de espera

        // Aguarda resposta da Raspberry Pi
        String receivedMessage = "";  // Variável local para a resposta
        unsigned long startTime = millis();
        while (millis() - startTime < 5000) {  // Aguarda até 5 segundos por uma resposta
          if (UART.available()) {
            receivedMessage = UART.readStringUntil('\n');
            if (!receivedMessage.isEmpty()) {
              resultFromRpi = receivedMessage;  // Atualiza a variável global
              Serial.println("Resposta da Raspberry Pi: " + resultFromRpi);
              break;  // Sai do loop ao receber a resposta
            }
          }
          vTaskDelay(pdMS_TO_TICKS(100));  // Pequeno atraso para evitar sobrecarga
        }

        if (receivedMessage.isEmpty()) {
          Serial.println("Nenhuma resposta recebida da Raspberry Pi.");
          resultFromRpi = "Erro: Sem resposta";  // Atualiza a variável global
        }

        // Atualiza o display com o resultado recebido ou erro
        updateDisplay("Luminosidade OK", resultFromRpi);
        waitingForResponse = false;  // Reseta o estado de espera
        vTaskDelay(pdMS_TO_TICKS(2000));  // Pequeno atraso para estabilidade
      }
    }

    vTaskDelay(pdMS_TO_TICKS(100));  // Pequeno atraso para estabilidade
  }
}

void setup() {
  Serial.begin(115200);  // Inicializa a comunicação serial para depuração
  UART.begin(115200, SERIAL_8N1, 16, 17);  // Inicializa a UART com pinos RX e TX

  // Inicializa o display OLED
  if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDRESS)) {
    Serial.println("Falha ao inicializar o display OLED!");
    while (1);  // Loop infinito se o display falhar
  }

  // Exibe mensagem inicial no display
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.println("Inicializando...");
  display.display();

  // Cria um mutex para acesso ao display
  mutex = xSemaphoreCreateMutex();
  if (mutex == NULL) {
    Serial.println("Falha ao criar o mutex!");
    while (1);  // Loop infinito se o mutex falhar
  }

  // Cria as tasks para rodar em núcleos diferentes
  xTaskCreatePinnedToCore(taskLDR, "TaskLDR", 2048, NULL, 1, NULL, 0);  // Core 0
  xTaskCreatePinnedToCore(taskTouchAndUART, "TaskTouchAndUART", 4096, NULL, 1, NULL, 1);  // Core 1
}

void loop() {
  // O loop principal não é usado porque as tarefas estão rodando no FreeRTOS
}

