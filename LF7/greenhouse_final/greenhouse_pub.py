import time
import board
import adafruit_dht
import RPi.GPIO as gpio
from paho.mqtt import client as mqtt_client

sensor = adafruit_dht.DHT22(board.D5,False)

broker = '172.17.0.108'
#broker = 'localhost'
port = 1883
topics = ["greenhouse/1/temp", "greenhouse/1/hum"] # Liste von topics die AN Etage2 gesendet werden
client_id = "Etage1_pub"

# Verbindung zum Broker
def connect_mqtt() -> mqtt_client:
    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id) # alte Version
    #client = mqtt_client.Client(client_id)
    while True:
        try:
            client.connect(broker, port)
            print("Connected to MQTT Broker!\n")
            break
        except Exception as e:
            print(f"Failed to connect to MQTT Broker: {e}")
            print("Attempting to reconnect in 5 seconds...")
            time.sleep(5)
    return client


#Publisher
def publish(client):
    while True:
        try:
            temperature_c = sensor.temperature
            humidity = sensor.humidity

            client.publish(temperature_c, topics[0], )
            client.publish(humidity, topics[1], )
            # print("Temp={0:0.1f}ºC, Humidity={1:0.1f}%".format(temperature_c, humidity))
            time.sleep(3)
        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
            time.sleep(1)
            continue
        except Exception as error:
            sensor.exit()
            raise error

def run():
    try:
        client = connect_mqtt()
        publish(client)
        client.loop_forever()
    except KeyboardInterrupt:
        print("Program terminated by user.")


if __name__ == '__main__':
    run()