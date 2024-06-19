# Detector de Movimiento Camuflado con Raspberry Pi Pico W

Este proyecto consiste en la creación de un detector de movimiento camuflado utilizando una Raspberry Pi Pico W. El dispositivo está diseñado para detectar movimientos utilizando un sensor de microondas RCWL-0516 y enviar notificaciones de detección de movimiento de manera inalámbrica a través de Wi-Fi. Además del sensor de movimiento, el dispositivo también está equipado con sensores de luz LDR y temperatura DS18B20 para obtener información adicional del entorno.

## Objetivos

- Crear un detector de movimiento discreto y camuflado.
- Utilizar una Raspberry Pi Pico W para agregar conectividad Wi-Fi al dispositivo.
- Implementar un sistema de notificación inalámbrica para informar sobre detecciones de movimiento.
- Integrar sensores de luz y temperatura para obtener información adicional del entorno.

## Instrucciones de Uso

1. Encienda el dispositivo y asegúrese de que esté conectado a una red Wi-Fi habiendo configurado correctamente el fichero config.py
2. El dispositivo comenzará a monitorear el entorno.
3. Si se desea empezar a monitorear movimiento manda /start al bot de Telegram y /stop si se desea parar de recibir notificaciones
3. Cuando se detecte movimiento, el dispositivo enviará una notificación a través de Wi-Fi al bot de Telegram.
4. También se pueden consultar los niveles de luz y temperatura mediante los comandos /temp y /luz al bot de Telegram

## Configuración del Hardware

- Raspberry Pi Pico W
- Sensor de Movimiento por Microondas RCWL-0516
- Sensor de Luz LDR
- Sensor de Temperatura DS18B20
- Batería Externa

## Configuración del Software

1. Clonar este repositorio en la Raspberry Pi Pico W.
2. Instalar las dependencias necesarias.
3. Modificar el fichero config con tus datos específicos
4. Ejecutar el programa principal.

