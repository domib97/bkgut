"""
Titel: Röntgenraum_Projekt
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

# Subscriber

# Constants
broker = "domipi"
port = 1883
topic = "zigbee/lamp"
lamp_id = "1"
deconz_api_url = "http://{zigbee_gateway_ip}:{port}/api/{your_api_key}"

# Logging
logging.basicConfig(level=logging.INFO)


# Lichtkontrolle  control_lamp(True) -> Lampe AN ; control_lamp(False) -> Lampe AUS
def control_lamp(turn_on: bool):

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


# MQTT
def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        logging.info("Connected to MQTT broker with result code " + str(rc))
    else:
        logging.error(f"Connection failed with result code {rc}")

    client.subscribe(topic)  # Subscribe after connection established


def on_message(msg):
    try:
        payload = msg.payload.decode()
        if payload.lower() == "on":
            control_lamp(True)  # Lampe AN
        elif payload.lower() == "off":
            control_lamp(False)  # Lampe AUS
        else:
            logging.warning(f"Unknown command: {payload}")
    except Exception as er:
        logging.error(f"Error processing message: {e}")


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
            print("\n:-)\n\nConnected to MQTT Broker!\nWaiting for Data:\n")
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
