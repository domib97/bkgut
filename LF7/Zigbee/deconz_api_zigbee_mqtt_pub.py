"""
Titel: deconz_api_zigbee_mqtt_pub.py
Organisation: BkGuT
Ersteller: Dan, Domi FISI-24
Lizenz: GPL-3.0, GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007
        Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
        Everyone is permitted to copy and distribute verbatim copies
        of this license document, but changing it is not allowed.
Sprachen/Protokolle:  Python, MQTT, Zigbee, HTTP requests, REST-API, logging
Datum: 30.05.2024
Module/Abhängigkeiten/docs/sources:"""
# https://dresden-elektronik.github.io/deconz-rest-doc/endpoints/sensors/#get-all-sensors
# https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
import time
import RPi.GPIO as GPIO
import logging
import requests
import paho.mqtt.client as mqtt  # Low-Level Lösung mit eigenem Client

# Konstanten
# MQTT
broker = "localhost"
port = 1883
client_id = "Lampe_Sub"
topics = ["zigbee/lamp", "zigbee/door"]
# Zigbee
lamp_id = "1"
sensor_id = "2"
sensor_api_url = "http://172.17.0.105/api/3C3719D085"
# GPIO setup
led_pin = 18
button_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)  # Output-Pin
GPIO.setup(button_pin, GPIO.IN)  # Input-Pin ohne internen Pull-Up/Down-Widerstand
# Logging
logging.basicConfig(level=logging.INFO)
# Flag, um den Zustand der LED zu steuern
led_flag = False


# Status der LED setzen
def set_led(state):
    global led_flag
    led_flag = state
    if led_flag:
        GPIO.output(led_pin, GPIO.HIGH)
    else:
        GPIO.output(led_pin, GPIO.LOW)


# Callback-Funktion, die bei einem Tastendruck aufgerufen wird
def button_callback(channel):
    global led_flag
    set_led(not led_flag)  # LED-Zustand umschalten


# Event-Detection für den Button einrichten
GPIO.add_event_detect(button_pin, GPIO.RISING, callback=button_callback, bouncetime=300)


# Sensorstatus abfragen
def get_sensor_status() -> int:
    url = f"{sensor_api_url}/sensors/{sensor_id}"
    try:
        response = requests.get(url)  # Get Request

        if response.status_code == 200:  # HTTP OK
            sensor_data = response.json()
            is_open = sensor_data['state']['open']
            status = "open" if is_open else "closed"
            logging.info(f"Sensor status: {status}")
        else:
            logging.error(f"Failed to get sensor status: {response.text}")  # HTTP ERROR
    except Exception as e:
        logging.error(f"Error getting sensor status: {e}")
    return is_open


# Publisher
def publish(client, turn_on: bool) -> None:
    state = "on" if turn_on else "off"  # Zustand
    client.publish(topics[0], state)


# MQTT Verbindung aufbauen
def connect_mqtt() -> mqtt.Client:
    obj_client = mqtt.Client()  # Client Objekterstellung
    while True:
        try:
            obj_client.connect(broker, port, 60)  # Verbindungsversuch zum Broker
            print("Connected to MQTT Broker!\nSending Data:\n")
            break
        except Exception as e:
            print(f"Failed to connect to MQTT Broker: {e}")
            print("Attempting to reconnect in 5 seconds...\n")
            time.sleep(5)
    return obj_client


# main Funktion
def main():
    try:
        # time.sleep(0.1)  # Kurze Verzögerung, um CPU-Last zu reduzieren
        obj_client = connect_mqtt()  # Verbindungsaufbau
        obj_client.loop_start()

        while True:
            publish(obj_client, turn_on=True) if get_sensor_status() else publish(obj_client, turn_on=False)
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nProgram terminated by user.\nStopping MQTT-Client loop\nExecute GPIO.cleanup")
    finally:
        obj_client.loop_stop()
        GPIO.cleanup()


if __name__ == '__main__':
    main()
