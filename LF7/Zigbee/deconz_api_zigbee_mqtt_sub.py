"""
Titel: deconz_api_zigbee_mqtt_sub.py
Organisation: BkGuT
Ersteller: Dan, Domi FISI-24
Lizenz: GPL-3.0, GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007
        Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
        Everyone is permitted to copy and distribute verbatim copies
        of this license document, but changing it is not allowed.
Sprachen/Protokolle: Python, MQTT, Zigbee, HTTP requests, REST-API
Datum: 30.05.2024
Module/Abhängigkeiten: <https://github.com/dresden-elektronik/deconz-rest-plugin>
"""
import time
import logging
import paho.mqtt.client as mqtt_alias
import requests
# import json //todo: Helligkeit über JSON dimmbar machen

# Konstanten
# MQTT
broker = "domipi"
port = 1883
topic = "zigbee/lamp"
client_id = "Lampe_Sub"

# Zigbee
# e.g 192.168.178.109/api/7B6BEDD305/lights/2
# "http://{zigbee_gateway_ip}:{port}/api/{your_api_key}"
lamp_id = "2"
deconz_api_url = "http://192.168.178.109/api/7B6BEDD305"

logging.basicConfig(level=logging.INFO)  # Logging


# deconz API Lichtkontrolle
# control_lamp(True) -> Lampe AN
# control_lamp(False) -> Lampe AUS
def control_lamp(turn_on: bool) -> None:

    # Zustand <https://dresden-elektronik.github.io/deconz-rest-doc/endpoints/lights/#set-light-state>
    state = "on" if turn_on else "off"

    # Set state REST-API URL
    url = f"{deconz_api_url}/lights/{lamp_id}/state"

    # Payload-Data im JSON Format
    data = {"on": turn_on}

    try:
        # Put Request <https://dresden-elektronik.github.io/deconz-rest-doc/getting_started/#turn-light-onoff>
        response = requests.put(url, json=data)

        if response.status_code == 200:  # HTTP OK
            logging.info(f"Lamp turned {state}")
        else:
            logging.error(f"Failed to turn {state} the lamp: {response.text}")  # HTTP ERROR
    except Exception as e:
        logging.error(f"Error controlling the lamp: {e}")


# Willkommensnachricht
def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        logging.info("Connected to MQTT broker with result code " + str(rc))
        print("\n#GoodVibesOnly\n:-)\n\nConnected to MQTT Broker!\nWaiting for Data:\n.\n.\n.\n")
    else:
        logging.error(f"Connection failed with result code {rc}")

    client.subscribe(topic)  # topic abonnieren wenn Verbindung aufgebaut


# Subscriber
def on_message(client, userdata, message):
    try:
        payload = message.payload.decode()  # Nutzlast dekodieren

        if payload.lower() == "on":  # Groß- und Kleinschreibung nicht berücksichtigt
            control_lamp(True)  # Lampe AN

        elif payload.lower() == "off":
            control_lamp(False)  # Lampe AUS

        else:
            print(f"Unknown command: {payload}")
    except Exception as er:
        print(f"Error processing message: {er}")


# MQTT Verbindung aufbauen
def connect_mqtt() -> mqtt_alias.Client:

    # Client Objekterstellung
    obj_client = mqtt_alias.Client(mqtt_alias.CallbackAPIVersion.VERSION2)

    obj_client.on_connect = on_connect
    obj_client.on_message = on_message

    # Verbindungsversuch zum Broker
    while True:
        try:
            obj_client.connect(broker, port, 60)
            logging.info("Connected to MQTT Broker!")
            break
        except Exception as e:
            logging.error(f"Failed to connect to MQTT Broker: {e}")
            logging.info("Attempting to reconnect in 5 seconds...")
            time.sleep(5)
    return obj_client
 

# main Funktion
def main():
    try:
        obj_client = connect_mqtt()  # Verbindungsaufbau
        obj_client.loop_forever()  # Endlosschleife
    except KeyboardInterrupt:
        logging.info("Program terminated by user.")


if __name__ == '__main__':
    main()
