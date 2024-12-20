import RPi.GPIO as GPIO
from gpiozero import RGBLED
from time import sleep
from mfrc522 import SimpleMFRC522
from colorzero import Color
led = RGBLED(17, 27, 22) 

GPIO.setwarnings(False)
#cria o objeto "leitor" para a instância "SimpleMFRC522" da biblioteca
leitor = SimpleMFRC522()
numeroUSP = "10310871"
print('Modo de leitura -> 1\n' )
print('Modo de escrita -> 2\n')
while True:
    x = input('Selecione o modo de funcionamento:\n')
    if x == '1':
        while True:
            print("Aproxime a tag do leitor para leitura.\n")
            id,texto = leitor.read()
            print("ID: {}\nTexto: {}".format(id, texto))
            if id == 497386497680:
                print("Acesso liberado.")
                led.color = Color('green')
            else:
                print("Acesso Negado.")
                led.color = Color('red')
            sleep(3) 
    elif x == '2':
        print("Aproxime a tag do leitor para gravar.\n")
        try:
            leitor.write(numeroUSP) 
            print("Concluído!")
            led.blink(on_time=0.3,off_time=0.3,on_color=(0,1,0))
            sleep(3)
            led.color = Color('black')
        except IndexError as IE:
            print("Falha na gravação: {IE}.\n")
            led.blink(on_time=0.3,off_time=0.3,on_color=(1,0,0))
            sleep(3)
            led.color = Color('black')
            continue
               
    else:
        print('Input inválido selecione 1 ou 2')
