import paho.mqtt.client as mqtt
import requests

# Configuration
broker = "domipi"
port = 1883
topic = "zigbee/lamp"
client_id = "Lampe_Pub_Sub"

deconz_api_url = "http://[zigbee_gateway_ip]:[port]/api/[your_api_key]"
lamp_id = "1"  # This is the ID of your IKEA lamp in the Deconz system


# Define the MQTT client callbacks
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


def run():
    try:

        client = mqtt.Client()  # Setup MQTT client
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect(broker, port, 60)  # Connect to the MQTT broker

        client.loop_forever()  # Blocking call processes network traffic, dispatches callbacks, handles reconnecting

    except KeyboardInterrupt:
        print("Program terminated by user.")


if __name__ == '__main__':
    run()
