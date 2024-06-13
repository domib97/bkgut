"""
Titel: deconz_api_zigbee_mqtt_sub.py
Organisation: BkGuT
Ersteller: Dan, Domi FISI-24
Lizenz: GPL-3.0, GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007
        Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
        Everyone is permitted to copy and distribute verbatim copies
        of this license document, but changing it is not allowed.
Sprachen/Protokolle: Python, MQTT, Zigbee, HTTP requests, REST-API, logging
Datum: 30.05.2024
Module/Abhängigkeiten/docs/sources:"""
# <https://github.com/dresden-elektronik/deconz-rest-plugin>
# <https://dresden-elektronik.github.io/deconz-rest-doc/endpoints/lights/#set-light-state>
# <https://dresden-elektronik.github.io/deconz-rest-doc/getting_started/#turn-light-onoff>
# e.g 192.168.178.109/api/7B6BEDD305/lights/2 -> "http://{zigbee_gateway_ip}:{port}/api/{your_api_key}"

import logging
import requests
import paho.mqtt.subscribe as subscribe  # High-Level Lösung ohne eigenem Client

# todo: Helligkeit über JSON dimmbar machen -> import json

# Konstanten
# MQTT
broker = "localhost"
port = 1883
client_id = "Lampe_Sub"
topics = ["zigbee/lamp", "zigbee/door"]

# Zigbee
lamp_id = "2"
deconz_api_url = "http://192.168.178.109/api/7B6BEDD305"

logging.basicConfig(level=logging.INFO)  # Logging


# Lichtkontrolle
# control_lamp(True) -> Lampe AN
# control_lamp(False) -> Lampe AUS
def control_lamp(turn_on: bool) -> None:
    state = "on" if turn_on else "off"  # Zustand
    url = f"{deconz_api_url}/lights/{lamp_id}/state"  # Set state URL
    data = {"on": turn_on}   # Payload-Data im JSON Format

    try:
        response = requests.put(url, json=data)  # Put Request

        if response.status_code == 200:  # HTTP OK
            logging.info(f"Lamp turned {state}")
        else:
            logging.error(f"Failed to turn {state} the lamp: {response.text}")  # HTTP ERROR
    except Exception as e:
        logging.error(f"Error controlling the lamp: {e}")


# Callback Funktion
def on_message(client, userdata, message) -> None:
    try:
        payload = message.payload.decode("utf-8")  # Nutzlast dekodieren

        if payload.lower() == "on":  # Groß- und Kleinschreibung wird nicht berücksichtigt
            control_lamp(True)  # Lampe AN

        elif payload.lower() == "off":
            control_lamp(False)  # Lampe AUS

        else:
            logging.error(f"Unknown command: {payload}")
    except Exception as er:
        logging.error(f"Error processing message: {er}")


# main Funktion
def main() -> None:
    try:
        print("\nWaiting for Data:\n.\n.\n.\n")
        subscribe.callback(on_message, topics, hostname=broker, qos=1)  # Subscriber mit Callback Funktion
    except Exception as e:
        logging.error(f"Failed to connect to MQTT Broker: {e}")
    except KeyboardInterrupt:
        logging.info("Program terminated by user.")


if __name__ == '__main__':
    main()
