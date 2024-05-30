import time
import paho.mqtt.client as mqtt
import requests

# MQTT-Config
broker = "domipi"
port = 1883
topic = "zigbee/lamp"
client_id = "Lampe_Pub_Sub"

# Zigbee-Config
deconz_api_url = "http://[zigbee_gateway_ip]:[port]/api/[your_api_key]"
lamp_id = "1"


# Zigbee
def control_lamp(turn_on):
    state = "on" if turn_on else "off"
    url = f"{deconz_api_url}/lights/{lamp_id}/state"
    data = {"on": turn_on}
    try:
        response = requests.put(url, json=data)
        if response.status_code == 200:
            print(f"Lamp turned {state}")
        else:
            print(f"Failed to turn {state} the lamp: {response.text}")
    except Exception as e:
        print(f"Error controlling the lamp: {e}")


# MQTT
def domi_mqtt():
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
        except Exception as e:
            print(f"Error processing message: {e}")

    obj_client = mqtt.Client()  # Client Objekterstellung

    obj_client.on_connect = on_connect
    obj_client.on_message = on_message

    obj_client.connect(broker, port, 60)  # Verbindung zum Broker

    obj_client.loop_forever()  # Endlosschleife


def run():
    try:
        domi_mqtt()
    except KeyboardInterrupt:
        print("Program terminated by user.")


if __name__ == '__main__':
    run()
