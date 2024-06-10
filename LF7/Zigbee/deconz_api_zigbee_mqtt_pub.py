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
import paho.mqtt.client as mqtt

# Konstanten
# MQTT
broker = "localhost"
port = 1883
client_id = "Lampe_Pub"
topics = ["zigbee/lamp", "zigbee/door"]
# todo topics = [("zigbee/lamp", 0), ("zigbee/door", 0)]

const_on = 'on'
const_off = 'off'


# Publisher
def publish(client, turn_on: bool) -> None:
    state = const_on if turn_on else const_off
    client.publish(topics[0], state)


# MQTT Verbindung aufbauen
def connect_mqtt() -> mqtt.Client:
    obj_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)  # Client Objekterstellung

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

        publish(obj_client, turn_on=True)
        print("Turn on")
        time.sleep(3)

        publish(obj_client, turn_on=False)
        print("Turn off")

        obj_client.loop_forever()  # Endlosschleife

    except KeyboardInterrupt:
        print("Program terminated by user.")


if __name__ == '__main__':
    main()
