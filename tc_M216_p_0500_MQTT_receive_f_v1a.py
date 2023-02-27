#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------
#           EPTM - Ecole professionnelle technique et des métiers
#
# Nom du fichier source              : tc_M216_p_0500_MQTT_send_f_v1a.py
#
# Auteur (Nom, Prénom)               : Jérémy Michaud
# Classe                             : MQTT_receive
# Module                             : M216
# Date de création                   : 30.01.2023
#
# Description succincte du programme :
#    Reçois des paquets MQTT selon les paramètres globaux
#----------------------------------------------------------------------------

import random

from paho.mqtt import client as mqtt_client


broker = 'mqtt-eptm.jcloud.ik-server.com'
port = 11521
topic = "JESFER/15"
max_qos = 2

# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = ''
password = ''


def connect_mqtt() -> mqtt_client:
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


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic, with qos `{msg.qos}` and retain `{msg.retain}`")

    client.subscribe(topic, max_qos)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
