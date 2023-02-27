import random
import time

from paho.mqtt import client as mqtt_client
from datetime import datetime

name  = 'JesFer'
sujet = 'M216'
broker = 'mqtt-eptm.jcloud.ik-server.com'
port = 11521
topic ="message/sport"
retain=False
print(f"creating topic '{topic}'")
qos=0

client_id = ''
username = ''
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
        result = client.publish(topic, msg, qos, retain)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()