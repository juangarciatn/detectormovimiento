from machine import Pin, Timer
from config import utelegram_config
from config import wifi_config
import time
import network
import utelegram
from ds18x20 import DS18X20
from onewire import OneWire

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(wifi_config['ssid'], wifi_config['password'])

ow = OneWire(Pin(14))
temp = DS18X20(ow)
rom = temp.scan()

SENSORMOV_PIN = 15
SENSORLUM_PIN = 16
usuarios = {}

def get_message(message):
    bot.send(message['message']['chat']['id'], message['message']['text'].upper())

def reply_start(message):
    global usuarios
    chat_id = message['message']['chat']['id']
    usuarios[chat_id] = True  # Agregar usuario al diccionario
    bot.send(message['message']['chat']['id'], 'Iniciando monitorización')
    
def reply_temp(message):
    temp.convert_temp()
    time.sleep(1)
    temperatura = temp.read_temp(rom[0])
    res = 'La temperatura es de ' + str(temperatura)
    print(temperatura)
    bot.send(message['message']['chat']['id'], res)
    
def reply_lum(message):
    sensorlum = Pin(SENSORLUM_PIN, Pin.IN).value()
    print(sensorlum)
    if sensorlum == 0:
        bot.send(message['message']['chat']['id'], 'La luz está encendida')
    else:
        bot.send(message['message']['chat']['id'], 'La luz está apagada')


def reply_stop(message):
    global usuarios
    chat_id = message['message']['chat']['id']
    if chat_id in usuarios:
        del usuarios[chat_id]
        


def detectar_movimiento(men):
    global usuarios
    for chat_id in usuarios.keys():  # Iterar sobre todos los usuarios registrados
        bot.send(chat_id, 'Movimiento detectado')

max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )
    led = Pin("LED", Pin.OUT)
    timer = Timer()

    def blink(timer):
        led.toggle()

    timer.init(freq=2.5, mode=Timer.PERIODIC, callback=blink)
    
    bot = utelegram.ubot(utelegram_config['token'])
    bot.register('/start', reply_start)
    bot.register('/temp', reply_temp)
    bot.register('/luz', reply_lum)
    bot.register('/stop', reply_stop)
    bot.set_default_handler(get_message)
    sensormov = Pin(SENSORMOV_PIN, Pin.IN)
    sensormov.irq(trigger=Pin.IRQ_RISING, handler=detectar_movimiento)
    print('BOT LISTENING')
    bot.listen()