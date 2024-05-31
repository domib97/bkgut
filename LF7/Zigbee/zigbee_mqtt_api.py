"""
Titel: Röntgenraum_Projekt
Organisation: BkGuT
Ersteller: Dan, Domi FISI-24
Lizenz: GPL-3.0, GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007
        Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
        Everyone is permitted to copy and distribute verbatim copies
        of this license document, but changing it is not allowed.
Sprachen/Protokolle: Python, MQTT, Zigbee, HTTP requests
Datum: 30.05.2024
Module/Abhängigkeiten: <https://github.com/dresden-elektronik/deconz-rest-plugin>
"""
import time
import paho.mqtt.client
import requests
# import json //todo: Helligkeit über JSON dimmbar machen


# MQTT-Config
broker = "domipi"
port = 1883
topic = "zigbee/lamp"
client_id = "Lampe_Pub_Sub"


# Zigbee/Deconz-Config
# <https://dresden-elektronik.github.io/deconz-rest-doc/getting_started/#acquire-an-api-key>
deconz_api_url = "http://[zigbee_gateway_ip]:[port]/api/[your_api_key]"
lamp_id = "1"  # <https://dresden-elektronik.github.io/deconz-rest-doc/endpoints/lights/>


# Lichtkontrolle  control_lamp(True) -> Lampe AN
def control_lamp(turn_on):

    # Zustand <https://dresden-elektronik.github.io/deconz-rest-doc/endpoints/lights/#set-light-state>
    state = "on" if turn_on else "off"

    # REST-API URL
    url = f"{deconz_api_url}/lights/{lamp_id}/state"

    # Payload-Data im JSON Format
    data = {"on": turn_on}

    try:
        # Put Request <https://dresden-elektronik.github.io/deconz-rest-doc/getting_started/#turn-light-onoff>
        response = requests.put(url, json=data)

        if response.status_code == 200:  # HTTP OK
            print(f"Lamp turned {state}")
        else:
            print(f"Failed to turn {state} the lamp: {response.text}")  # HTTP ERROR
    except Exception as e:
        print(f"Error controlling the lamp: {e}")


# MQTT
def domi_mqtt_sub():
    def on_connect(client, rc):
        print("Connected to MQTT broker with result code " + str(rc))
        client.subscribe(topic)

    # MQTT Subscriber
    def on_message(msg):
        try:
            payload = msg.payload.decode()

            if payload.lower() == "on":
                control_lamp(True)  # Lampe AN

            elif payload.lower() == "off":
                control_lamp(False)  # Lampe AUS

            else:
                print(f"Unknown command: {payload}")
        except Exception as er:
            print(f"Error processing message: {er}")

    def connect_mqtt() -> mqtt_client:
        # client = mqtt_client.Client(client_id)
        client = paho.mqtt.client.Client(paho.mqtt.client.CallbackAPIVersion.VERSION1)
        while True:
            try:
                client.connect(broker, port)
                print("Connected to MQTT Broker!\n")
                break
            except Exception as e:
                print(f"Failed to connect to MQTT Broker: {e}")
                print("Attempting to reconnect in 5 seconds...\n")
                time.sleep(5)
        return client

    # Client Objekterstellung
    obj_client = paho.mqtt.client.Client(paho.mqtt.client.CallbackAPIVersion.VERSION1)

    obj_client.on_connect = on_connect
    obj_client.on_message = on_message

    # Verbindungsversuch zum Broker
    while True:
        try:
            obj_client.connect(broker, port, 60)
            print("Connected to MQTT Broker!\nWaiting for Data:\n")
            break
        except Exception as e:
            print(f"Failed to connect to MQTT Broker: {e}")
            print("Attempting to reconnect in 5 seconds...")
            time.sleep(5)
    # Endlosschleife
    obj_client.loop_forever()


# main Funktion
def main():
    try:
        domi_mqtt_sub()
    except KeyboardInterrupt:
        print("Program terminated by user.")


if __name__ == '__main__':
    main()
