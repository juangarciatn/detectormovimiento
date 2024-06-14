from machine import Pin, Timer
from config import utelegram_config
from config import wifi_config
from config import mqtt_config
import time
import network
import utelegram
from ds18x20 import DS18X20
from onewire import OneWire
from umqtt.simple import MQTTClient

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(wifi_config['ssid'], wifi_config['password'])

ow = OneWire(Pin(14))
temp = DS18X20(ow)
rom = temp.scan()

SENSORMOV_PIN = 15
SENSORLUM_PIN = 16
usuarios = {}
timer = Timer()
led = Pin("LED", Pin.OUT)
sensormov = Pin(SENSORMOV_PIN, Pin.IN)

def mqtt_connect():
    global client
    client = MQTTClient(mqtt_config['client_id'], mqtt_config['mqtt_server'], keepalive=3600)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_config['mqtt_server']))
    return client

def send_mqtt(timer):
    temp.convert_temp()
    temperatura = temp.read_temp(rom[0])
    time.sleep(1)
    print('temperatura enviada: ', str(temperatura))
    client.publish(mqtt_config['topic_pub'], str(temperatura))

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
    send_mqtt(timer)
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
    bot.send(message['message']['chat']['id'], 'Deteniendo monitorización')
        


def detectar_movimiento(men):
    global usuarios
    for chat_id in usuarios.keys():  # Iterar sobre todos los usuarios registrados
        bot.send(chat_id, 'Movimiento detectado')
    led.value(1)
    time.sleep(2)
    led.value(0)

sensormov.irq(trigger=Pin.IRQ_RISING, handler=detectar_movimiento)

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
    mqtt_connect()

    bot = utelegram.ubot(utelegram_config['token'])
    bot.register('/start', reply_start)
    bot.register('/temp', reply_temp)
    bot.register('/luz', reply_lum)
    bot.register('/stop', reply_stop)
    bot.set_default_handler(get_message)
    timer.init(freq=1/300, mode=Timer.PERIODIC, callback=send_mqtt)
    print('BOT LISTENING')
    bot.listen()