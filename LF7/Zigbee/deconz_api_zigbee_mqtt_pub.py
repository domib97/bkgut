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

# Publisher

# MQTT-Config
broker = "domipi"
port = 1883
# topics = [("zigbee/lamp", 0), ("zigbee/door", 0)]
topics = ["zigbee/lamp", "greenhouse/1/hum"]
topic = "zigbee/lamp"
client_id = "Lampe_Pub"


# Zigbee/Deconz-Config
# <https://dresden-elektronik.github.io/deconz-rest-doc/getting_started/#acquire-an-api-key>
deconz_api_url = "http://[zigbee_gateway_ip]:[port]/api/[your_api_key]"
lamp_id = "1"


# Lichtkontrolle  control_lamp(True) -> Lampe AN ; control_lamp(False) -> Lampe AUS
def control_lamp(turn_on):

    # Zustand <https://dresden-elektronik.github.io/deconz-rest-doc/endpoints/lights/#set-light-state>
    state = "on" if turn_on else "off"

    # 0Set state REST-API URL
    # url = f"{deconz_api_url}/lights/{lamp_id}/state"

    # Payload-Data im JSON Format
    # data = {"on": turn_on}

    # response = requests.put(url, json=data)

# MQTT
def on_connect(client, userdata, flags, rc, properties):
    # **No arguments for on_connect!**
    print("Connected to MQTT broker with result code " + str(rc))
    client.subscribe(topic)  # Subscribe after connection established



# Publisher
def publish(client):
    while True:
        try:
            # Lichtkontrolle  control_lamp(True) -> Lampe AN ; control_lamp(False) -> Lampe AUS
            
            if ():
                flag: bool = True
            elif ():
                flag: bool = False

            const_on: str = 'on'
            const_off: str = 'off'

            if flag:  # if flag == True
                client.publish(topics[0], const_on)
            elif not flag:
                client.publish(topics[0], const_off)
            else:
                return 0
        finally:
            return 0


def connect_mqtt() -> mqtt_alias.Client:

    # Client Objekterstellung
    obj_client = mqtt_alias.Client(mqtt_alias.CallbackAPIVersion.VERSION2)

    obj_client.on_connect = on_connect

    # Verbindungsversuch zum Broker
    while True:
        try:
            obj_client.connect(broker, port, 60)
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
        publish(obj_client)
        obj_client.loop_forever()  # Endlosschleife
    except KeyboardInterrupt:
        print("Program terminated by user.")


if __name__ == '__main__':
    main()
