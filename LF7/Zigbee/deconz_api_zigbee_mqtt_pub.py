"""
Titel: deconz_api_zigbee_mqtt_pub.py
Organisation: BkGuT
Ersteller: Dan, Domi FISI-24
Lizenz: GPL-3.0, GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007
        Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
        Everyone is permitted to copy and distribute verbatim copies
        of this license document, but changing it is not allowed.
Sprachen/Protokolle: Python, MQTT, Zigbee, HTTP requests, REST-API
Datum: 30.05.2024
Module/Abhängigkeiten/docs:"""

import time
import paho.mqtt.client as mqtt_alias
import paho.mqtt.publish as publish  # High-Level Lösung

# Konstanten
# MQTT
broker = "domipi"
port = 1883
client_id = "Lampe_Pub"
topics = ["zigbee/lamp", "zigbee/door"]

# //todo topics = [("zigbee/lamp", 0), ("zigbee/door", 0)]


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


# MQTT Verbindung aufbauen
def connect_mqtt() -> mqtt_alias.Client:

    # Client Objekterstellung
    obj_client = mqtt_alias.Client(mqtt_alias.CallbackAPIVersion.VERSION2)

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

"""
# Zugriffsdaten für MQTT-Broker und andere Konfigurationsdaten
print("Zugriffs- und Konfigurationsdaten festlegen")
# URL = "test.mosquitto.org"    # Public free MQTT Broker
URL = "localhost"    # Lokaler MQTT Broker
INTERVALL = 2


# Werte an MQTT-Broker senden
print("Werte an MQTT-Broker senden")
sensor = wg.LuftSensor()
while True:
    temperatur = sensor.temperatur()
    luftfeuchtigkeit = sensor.luftfeuchtigkeit()
    publish.single("bkgut/test/temperatur", temperatur, hostname=URL, qos=1)
    publish.single("bkgut/test/luftfeuchtigkeit", luftfeuchtigkeit, hostname=URL, qos=1)
    print(".", end="")
    time.sleep(INTERVALL)
"""


# main Funktion
def main():
    try:
        obj_client = connect_mqtt()  # Verbindungsaufbau

        for x in range(1, 4, 1):
            print(str(x) + "\tSekunden...")
            time.sleep(1)

        def on_off_on():  # eine Funktion die das Licht, EIN, AUS und wieder EIN schaltet
            time.sleep(0.5)
            publish(obj_client, turn_on=True)
            print("Turned on")
            time.sleep(1.5)
            publish(obj_client, turn_on=False)
            print("Turned off")
            time.sleep(1.5)
            publish(obj_client, turn_on=True)
            print("Turned on")

        on_off_on()

        time.sleep(3)
        obj_client.loop_forever()  # Endlosschleife

    except KeyboardInterrupt:
        print("Program terminated by user.")


if __name__ == '__main__':
    main()
