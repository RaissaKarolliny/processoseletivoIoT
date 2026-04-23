
from machine import Pin, PWM, I2C
from micropython import const
import framebuf
import time

# código pro display funcionar, pois não consegui importa a biblioteca
SET_CONTRAST = const(0x81)
SET_ENTIRE_ON = const(0xa4)
SET_NORM_INV = const(0xa6)
SET_DISP = const(0xae)
SET_MEM_ADDR = const(0x20)
SET_COL_ADDR = const(0x21)
SET_PAGE_ADDR = const(0x22)
SET_DISP_START_LINE = const(0x40)
SET_SEG_REMAP = const(0xa0)
SET_MUX_RATIO = const(0xa8)
SET_COM_OUT_DIR = const(0xc0)
SET_DISP_OFFSET = const(0xd3)
SET_COM_PIN_CFG = const(0xda)
SET_DISP_CLK_DIV = const(0xd5)
SET_PRECHARGE = const(0xd9)
SET_VCOM_DESEL = const(0xdb)
SET_CHARGE_PUMP = const(0x8d)

class SSD1306_I2C:
    def __init__(self, width, height, i2c, addr=0x3C):
        self.width = width
        self.height = height
        self.i2c = i2c
        self.addr = addr
        self.buffer = bytearray(self.height // 8 * self.width)
        self.framebuf = framebuf.FrameBuffer(self.buffer, self.width, self.height, framebuf.MONO_VLSB)
        self.init_display()

    def write_cmd(self, cmd):
        self.i2c.writeto(self.addr, bytearray([0x80, cmd]))

    def write_data(self, buf):
        self.i2c.writeto(self.addr, b'\x40' + buf)

    def init_display(self):
        for cmd in (
            SET_DISP | 0x00,
            SET_MEM_ADDR, 0x00,
            SET_DISP_START_LINE | 0x00,
            SET_SEG_REMAP | 0x01,
            SET_MUX_RATIO, self.height - 1,
            SET_COM_OUT_DIR | 0x08,
            SET_DISP_OFFSET, 0x00,
            SET_COM_PIN_CFG, 0x12,
            SET_DISP_CLK_DIV, 0x80,
            SET_PRECHARGE, 0xf1,
            SET_VCOM_DESEL, 0x30,
            SET_CONTRAST, 0xff,
            SET_ENTIRE_ON,
            SET_NORM_INV,
            SET_CHARGE_PUMP, 0x14,
            SET_DISP | 0x01,
        ):
            self.write_cmd(cmd)

    def fill(self, col):
        self.framebuf.fill(col)

    def text(self, string, x, y):
        self.framebuf.text(string, x, y)

    def show(self):
        self.write_cmd(SET_COL_ADDR)
        self.write_cmd(0)
        self.write_cmd(self.width - 1)
        self.write_cmd(SET_PAGE_ADDR)
        self.write_cmd(0)
        self.write_cmd(self.height // 8 - 1)
        self.write_data(self.buffer)

#display
i2c = I2C(0, scl=Pin(22), sda=Pin(15))
oled = SSD1306_I2C(128, 64, i2c)


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

#função pra mostrar a mensagem no display
def mostrar_mensagem(l1, l2=""):
    oled.fill(0)
    oled.text(l1, 0, 0)
    oled.text(l2, 0, 20)
    oled.show()

#desliga todos os leds
def desligar_todos():
    led_azul.off()
    led_vermelho.off()
    led_verde.off()
#aciona o led, depois desliga e liga 5 vezes
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
    mostrar_mensagem("PRECISO DE", "AJUDA")
    som_urgente()
    acionar(led_vermelho)
    print("Ação: Preciso de ajuda")

def acao_banheiro():
    mostrar_mensagem("IR AO", "BANHEIRO")
    som_curto()
    acionar(led_azul)
    print("Ação: Ir ao banheiro")

def acao_ok():
    mostrar_mensagem("ESTOU", "BEM")
    som_longo()
    acionar(led_verde)
    print("Ação: Estou bem")
    
# função para ler os botões e executar a ação correspondente.
# como estou usando a simulação essa função não é chmada. 
# Seria utilizada em um loop infinito para ficar lendo os botões constantemente em um ambiente não simulado.
def ler_botoes():
    if botao_vermelho.value() == 0:
        acao_ajuda()
        time.sleep(0.3)  # debounce

    elif botao_azul.value() == 0:
        acao_banheiro()
        time.sleep(0.3)

    elif botao_verde.value() == 0:
        acao_ok()
        time.sleep(0.3)  

#função para simular o teste automático 
def modo_teste():
    print("Iniciando teste automático")

    acao_ajuda()
    acao_banheiro()
    acao_ok()

    print("SIMULACAO_OK")

modo_teste()
        
