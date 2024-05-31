import time
from paho.mqtt import client as mqtt_client

broker = 'domipi'
port = 1883
topics = ["greenhouse/1/temp", "greenhouse/1/hum"]  # Liste von topics die AN Etage2 gesendet werden
client_id = "Etage1_pub"


# Verbindung zum Broker
def class_connect_mqtt():
    client = mqtt_client.Client()
    #  client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1)
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


def run():
    try:
        print("Blub")
        obj_client = class_connect_mqtt()
        obj_client.loop_forever()
    except KeyboardInterrupt:
        print("Program terminated by user.")


if __name__ == '__main__':
    run()
