# SEL0337

![GitHub repo size](https://img.shields.io/github/repo-size/fernandohpra/SEL0337)
![GitHub language count](https://img.shields.io/github/languages/count/fernandohpra/SEL0337)
![GitHub forks](https://img.shields.io/github/forks/fernandohpra/SEL0337)



## Prática 5
Para a prática 5 o código desenvolvido na prática 4 para acesso RFID foi utilizado.

### 💻 Dependências
Bibliotecas:
- [x] RPi.GPIO
- [x] gpiozero
- [x] time
- [x] mfrc522
- [x] colorzero
<img src="dependências e saídas.png" alt="Dependências e pinos de saída do código">

### 🚀 Funcionamento
O código foi feito para que o leitor RFID se inicie com o linux via systemD, a principio o código foi feito de forma a autorizar apenas uma RFID e funcionar contantemente até que a leitura dessa RFID específica seja realizada.
De forma geral é um código que faria parte de um sistema maior, como um aplicativo que só deve funcionar sobre autorização, sendo apenas uma prova de conceito.
<img src="autenticador.png" alt="Código do autenticador">
O programa contantemente aguarda a leitura de um tag RFID, indicado pelo LED aceso com cor amerela, após a leitura de uma tag é verificado se o ID da tag corresponde ao ID estabelecido no código. Caso a tag seja autorizada o programa aciona o LED com a luz verde e retorna 0, caso contrário o LED é acionado com luz vermelha e o programa volta para o loop principal após 3 segundos.
Por segurança, pois trata-se algo relacionado a inicialização do sistema, foi adicionado uma interrupção pelo teclado a fim de evitar qualquer tipo de erro não esperado na inicialização devido ao autenticador.

<img src="finalprat5.png" alt="Parte final do código">
Por fim garante-se que o código só funcionará quando executador diretamente, parte vestigial do código feita para testar as funcionalidades do systemD que foi mantida por não afetar o funcionamento do código.

<img src="service.png" alt="Service">
O .service feito para essa prática é bem simples e segue o padrão dos exemplos de aula, para utilizações práticas adionaria-se um ExecStop para executar o programa desejado após a autenticação.
Por motivos ainda não esclarecidos o programa não funciona na raspberry PI com o endereço do resposítorio, forçando que o código fosse colocado em /home/sel/ como indicado pelo .service.
