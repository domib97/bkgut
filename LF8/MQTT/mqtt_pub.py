import time
from paho.mqtt import client as mqtt_client

broker = 'domipi'
port = 1883
topics = ["greenhouse/1/temp", "greenhouse/1/hum"]  # Liste von topics die AN Etage2 gesendet werden
client_id = "Etage1_pub"


# Verbindung zum Broker
def connect_mqtt() -> mqtt_client:
    # client = mqtt_client.Client(client_id)
    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1)
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


# Publisher
def publish(client):
    while True:
        try:
            print("Blub")
            time.sleep(3)
        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
            time.sleep(1)
            continue
        except Exception as error:
            # sensor.exit()
            raise error


def run():
    try:
        client = connect_mqtt()
        # publish(client)
        client.loop_forever()
    except KeyboardInterrupt:
        print("Program terminated by user.")


if __name__ == '__main__':
    run()
