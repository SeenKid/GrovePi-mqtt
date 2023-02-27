#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
#           EPTM - Ecole professionnelle technique et des métiers
#
# Nom du fichier source              : tc_M216_p_0500_MQTT_send_f_v1a.py
#
# Auteur (Nom, Prénom)               : Jérémy Michaud
# Classe                             : MQTT_send
# Module                             : M216
# Date de création                   : 30.01.2023
#
# Description succincte du programme :
#   Envoie des paquets MQTT selon les paramètres globaux
#----------------------------------------------------------------------------

import random
import time
from grovepi import *

from paho.mqtt import client as mqtt_client


broker = 'mqtt-eptm.jcloud.ik-server.com'
port = 11521
topic = "led/12"
retain=False
led = 3
qos=0

# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
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
        msg = f"messages: {msg_count}"
        var = input("Entrez une valeur pour la puissance de la led entre 1 et 255 :")
        int(var)
        int(led)
        analogWrite(led, int(var))
        result = client.publish(topic, msg, qos, retain)
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

    analogWrite(led, int(msg))


def run():
    client = connect_mqtt()
    client.loop_start()
    subscribe(client)
    client.loop_forever()
    publish(client)


if __name__ == '__main__':
    run()
