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
import paho.mqtt.client as mqtt_alias
import requests

# Subscriber

# MQTT-Config
broker = "domipi"
port = 1883
topic = "zigbee/lamp"
client_id = "Lampe_Sub"


# Zigbee/Deconz-Config
# <https://dresden-elektronik.github.io/deconz-rest-doc/getting_started/#acquire-an-api-key>
deconz_api_url = "http://[zigbee_gateway_ip]:[port]/api/[your_api_key]"
lamp_id = "1"


# Lichtkontrolle  control_lamp(True) -> Lampe AN ; control_lamp(False) -> Lampe AUS
def control_lamp(turn_on):

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
            print(f"Lamp turned {state}")
        else:
            print(f"Failed to turn {state} the lamp: {response.text}")  # HTTP ERROR
    except Exception as e:
        print(f"Error controlling the lamp: {e}")


# MQTT
def on_connect(client, userdata, flags, rc, properties):
    # **No arguments for on_connect!**
    print("Connected to MQTT broker with result code " + str(rc))
    client.subscribe(topic)  # Subscribe after connection established


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


def connect_mqtt() -> mqtt_alias.Client:

    # Client Objekterstellung
    obj_client = mqtt_alias.Client(mqtt_alias.CallbackAPIVersion.VERSION2)

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
            print("Attempting to reconnect in 5 seconds...\n")
            time.sleep(5)
    return obj_client


# main Funktion
def main():
    try:
        obj_client = connect_mqtt()  # Verbindungsaufbau
        obj_client.loop_forever()  # Endlosschleife
    except KeyboardInterrupt:
        print("Program terminated by user.")


if __name__ == '__main__':
    main()
