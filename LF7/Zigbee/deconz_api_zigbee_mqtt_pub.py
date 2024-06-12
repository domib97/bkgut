"""
Titel: deconz_api_zigbee_mqtt_pub.py
Organisation: BkGuT
Ersteller: Dan, Domi FISI-24
Lizenz: GPL-3.0, GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007
        Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
        Everyone is permitted to copy and distribute verbatim copies
        of this license document, but changing it is not allowed.
Sprachen/Protokolle: Python, MQTT
Datum: 30.05.2024
Module/Abhängigkeiten: time, paho.mqtt.client
"""

import time
import logging
import requests
import paho.mqtt.client as mqtt

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

logging.basicConfig(level=logging.INFO)  # Logging


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
        obj_client = connect_mqtt()  # Verbindungsaufbau
        obj_client.loop_start()

        publish(obj_client, turn_on=True) if get_sensor_status() else publish(obj_client, turn_on=False)

        obj_client.loop_forever()  # Endlosschleife

    except KeyboardInterrupt:
        print("Program terminated by user.")


if __name__ == '__main__':
    main()
