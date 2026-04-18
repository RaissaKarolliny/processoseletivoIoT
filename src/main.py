
from machine import Pin, PWM
import time
import sys

# LEDs
led_azul = Pin(4, Pin.OUT)
led_vermelho = Pin(2, Pin.OUT)
led_verde = Pin(21, Pin.OUT)

# Botões
botao_azul = Pin(18, Pin.IN, Pin.PULL_UP)
botao_vermelho = Pin(5, Pin.IN, Pin.PULL_UP)
botao_verde = Pin(19, Pin.IN, Pin.PULL_UP)

# Buzzer
buzzer = PWM(Pin(22))
buzzer.duty(0)

def desligar_todos():
    led_azul.off()
    led_vermelho.off()
    led_verde.off()

def acionar(led):
    desligar_todos()
    led.on()
    time.sleep(0.2) 
    for _ in range(5):  
        led.off()
        time.sleep(0.1)
        led.on()
        time.sleep(0.1) 
    led.off()

def som_curto():  # banheiro
    buzzer.freq(1000)
    buzzer.duty(512)
    time.sleep(0.1)
    buzzer.duty(0)

def som_longo():  #Estou com Fome
    buzzer.freq(800)
    buzzer.duty(512)
    time.sleep(0.15)
    buzzer.duty(0)

def som_urgente():  # ajuda
    buzzer.freq(1500)
    for _ in range(3):
        buzzer.duty(512)
        time.sleep(0.10)
        buzzer.duty(0)
        time.sleep(0.10)

def acao_ajuda():
    som_urgente()
    acionar(led_vermelho)
    print("Ação: Preciso de ajuda")

def acao_banheiro():
    som_curto()
    acionar(led_azul)
    print("Ação: Ir ao banheiro")

def acao_ok():
    som_longo()
    acionar(led_verde)
    print("Ação: Estou bem")

def modo_teste():
    print("Iniciando teste automático")

    acao_ajuda()
    acao_banheiro()
    acao_ok()

    print("SIMULACAO_OK")
    time.sleep(1)
    sys.exit()

modo_teste()
        
