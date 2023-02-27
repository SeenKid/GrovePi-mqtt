import random
import time

from paho.mqtt import client as mqtt_client
from datetime import datetime

name  = 'YannBerl'
sujet = 'X'
broker = 'mqtt-eptm.jcloud.ik-server.com'
port = 11521
topic = input("Entrez le topic : ")
username = input("Entrez votre nom : ")
retain=False
print(f"talking in topic : '{topic}'")
qos=0
max_qos = 2


client_id = ''
password = ''

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 0
    while True:
        time.sleep(1)
        msg = input('Enter message:')
        result = client.publish(topic, username +" - "+ msg, qos, retain)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic, with qos `{msg.qos}` and retain `{msg.retain}`")

    client.subscribe(topic, max_qos)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    client.loop_start()
    subscribe(client)
    publish(client)
    


if __name__ == '__main__':
    run()