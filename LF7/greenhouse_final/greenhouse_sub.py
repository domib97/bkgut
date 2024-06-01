import time
from paho.mqtt import client as mqtt_client
import RPi.GPIO as gpio

servo_pin = 20
gpio.setmode(gpio.BCM)
gpio.setup(servo_pin, gpio.OUT)

broker = '172.17.0.108'
#broker = 'localhost'
port = 1883
topics = [("greenhouse/2/temp", 0), ("greenhouse/2/hum", 0)] # Tupel von topics die VON Etage2 gesendet werden mit QoS
client_id = "Etage1_sub"

def luke_auf():
    p = gpio.PWM(servo_pin, 50)
    p.start(2.5)
    p.ChangeDutyCycle(7.5)
    time.sleep(1)
    p.stop()

def luke_zu():
    p = gpio.PWM(servo_pin, 50)
    p.start(2.5)
    p.ChangeDutyCycle(2.5)
    time.sleep(1)
    p.stop()

# Verbindung zum Broker
def connect_mqtt() -> mqtt_client:
    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id) # alte Version
    #client = mqtt_client.Client(client_id)
    while True:
        try:
            client.connect(broker, port)
            print("Connected to MQTT Broker!\nWaiting for Data:\n")
            break
        except Exception as e:
            print(f"Failed to connect to MQTT Broker: {e}")
            print("Attempting to reconnect in 5 seconds...")
            time.sleep(5)
    return client

# Subscriber
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        if (float(msg.payload.decode()) >= 23 and str(msg.topic) == "greenhouse/2/temp"):
            print("Temp über 23 C")
        elif (float(msg.payload.decode()) >=65  and str(msg.topic) == "greenhouse/2/hum"):
            print("Humidity über 65 % Luke AUF")
            luke_auf()
        elif (float(msg.payload.decode()) <=65  and str(msg.topic) == "greenhouse/2/hum"):
            print("Humidity unter 65 % Luke ZU")
            luke_zu()
        else:
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")


    client.subscribe(topics) # Subscribing von multiplen topics
    client.on_message = on_message
    
def run():
    try:
        client = connect_mqtt()
        subscribe(client)
        client.loop_forever()
    except KeyboardInterrupt:
        print("Program terminated by user.")

if __name__ == '__main__':
    run()