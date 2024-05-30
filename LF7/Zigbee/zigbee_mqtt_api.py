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
Module/Abhängigkeiten:
"""
import time
import paho.mqtt.client as mqtt
import requests

# MQTT-Config
broker = "domipi"
port = 1883
topic = "zigbee/lamp"
client_id = "Lampe_Pub_Sub"

# Zigbee-Config <https://dresden-elektronik.github.io/deconz-rest-doc/getting_started/>
deconz_api_url = "http://[zigbee_gateway_ip]:[port]/api/[your_api_key]"
lamp_id = "1"


# Zigbee Lichtkontrolle <https://dresden-elektronik.github.io/deconz-rest-doc/endpoints/lights/>
def control_lamp(turn_on):
    url = f"{deconz_api_url}/lights/{lamp_id}/state"  # REST-API URL

    state = "on" if turn_on else "off"  # Zustand

    data = {"on": turn_on}  # JSON Format
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

    def on_message(msg):
        try:
            payload = msg.payload.decode()
            if payload.lower() == "on":
                control_lamp(True)
            elif payload.lower() == "off":
                control_lamp(False)
            else:
                print(f"Unknown command: {payload}")
        except Exception as er:
            print(f"Error processing message: {er}")

    # Client Objekterstellung
    obj_client = mqtt.Client()

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


# Main Funktion
def main():
    try:
        domi_mqtt_sub()
    except KeyboardInterrupt:
        print("Program terminated by user.")


if __name__ == '__main__':
    main()
