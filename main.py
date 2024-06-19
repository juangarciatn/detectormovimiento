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

usuarios = {}
timer = Timer()

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(wifi_config['ssid'], wifi_config['password'])

    max_attempts = 10
    attempt = 0
    while attempt < max_attempts and not wlan.isconnected():
        print('Attempting to connect to WiFi...')
        attempt += 1
        time.sleep(1)

    if wlan.isconnected():
        print('Connected to WiFi')
    else:
        raise Exception('Failed to connect to WiFi')
    return wlan

def mqtt_connect():
    global client
    client = MQTTClient(mqtt_config['client_id'], mqtt_config['mqtt_server'], keepalive=3600)
    client.connect()
    print('Connected to %s MQTT Broker' % (mqtt_config['mqtt_server']))
    return client

def send_mqtt(timer):
    temp.convert_temp()
    temperatura = temp.read_temp(rom[0])
    time.sleep(1)
    print('temperatura enviada: ', str(temperatura))
    client.publish(mqtt_config['topic_pub'], str(temperatura))

def reply_start(message):
    global usuarios
    chat_id = message['message']['chat']['id']
    usuarios[chat_id] = True  # Agregar usuario al diccionario
    bot.send(message['message']['chat']['id'], 'Iniciando monitorización')
    
def reply_stop(message):
    global usuarios
    chat_id = message['message']['chat']['id']
    if chat_id in usuarios:
        del usuarios[chat_id]
    bot.send(message['message']['chat']['id'], 'Deteniendo monitorización')

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

def detectar_movimiento(men):
    global usuarios
    for chat_id in usuarios.keys():  # Iterar sobre todos los usuarios registrados
        bot.send(chat_id, 'Movimiento detectado')
    led.value(1)
    time.sleep(2)
    led.value(0)

# Conectar a WiFi
wlan = connect_wifi()

# Configurar sensores y MQTT
ow = OneWire(Pin(14))
temp = DS18X20(ow)
rom = temp.scan()

SENSORMOV_PIN = 15
SENSORLUM_PIN = 16
usuarios = {}
timer = Timer()
led = Pin("LED", Pin.OUT)
sensormov = Pin(SENSORMOV_PIN, Pin.IN)

sensormov.irq(trigger=Pin.IRQ_RISING, handler=detectar_movimiento)

mqtt_connect()

# Configurar y lanzar el bot de Telegram
bot = utelegram.ubot(utelegram_config['token'])
bot.register('/start', reply_start)
bot.register('/stop', reply_stop)
bot.register('/temp', reply_temp)
bot.register('/luz', reply_lum)
print("BOT LISTEN")
bot.listen()