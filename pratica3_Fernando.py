import RPi.GPIO as GPIO
import lgpio
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(17,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setwarnings(False)
GPIO.output(18, False)
chip = lgpio.gpiochip_open(0)

lgpio.gpio_claim_output(chip, 18)
lgpio.gpio_claim_input(chip, 17)

def button(pin):
    if GPIO.input(pin):
        GPIO.output(18, False)
    else:
        GPIO.output(18, True)

def contagem_regressiva(tempo):
    minutos, segundos =divmod(tempo,60)
    while tempo:
        print(f'{minutos:02d}:{segundos:02d}', end= '\r')
        sleep(1)
        tempo -= 1
        minutos, segundos =divmod(tempo,60)
    print("\nAcendendo LED.")
    GPIO.output(18, True)
    
def receber_tempo():
    while True:
        try:
            tempo = int(input("Digite o tempo em segundos: "))
            if tempo <= 0:
                raise ValueError("O numero deve ser positivo")
            return tempo
        except ValueError as e:
            print(f"Erro, insira um numero valido")
            
def set_mode(modo):
    if modo == 1:
        print("Modo 1: LED ao pressionar o botao")
        GPIO.add_event_detect(17, GPIO.RISING, callback=button, bouncetime=200)
    
    elif modo ==2:
        print("Modo 2: LED com delay ao pressionar o botao")
        tempo = receber_tempo()
        print("Pressione o botao para iniciar a contagem")
        while GPIO.input(17):
            sleep(0.1)
        print("Iniciando contagem")
        contagem_regressiva(tempo)
    else:
        print("Entrada invalida, selecione 1 ou 2.")
        
        
entrada = int(input("Digite 1 para botao normal e 2 para botao com delay: "))
set_mode(entrada)

try:
    while True:
        sleep(0.1)
except KeyboardInterrupt:
    print("Encerrando o programa")
finally:
    GPIO.cleanup()
