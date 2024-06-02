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


# MQTT
def on_connect(client, userdata, flags, rc, properties):
    # **No arguments for on_connect!**
    print("Connected to MQTT broker with result code " + str(rc))
    client.subscribe(topic)  # Subscribe after connection established


# Publisher
def publish(client, turn_on: bool) -> int:
    while True:
        try:
            const_on: str = 'on'
            const_off: str = 'off'

            state = "on" if turn_on else "off"

            if state == "on":
                flag = True
                client.publish(topics[0], const_on)
            elif state == "off":
                flag = False
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

        for x in range(1, 4, 1):
            print(str(x) + "\tSekunden...")
            time.sleep(1)

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
