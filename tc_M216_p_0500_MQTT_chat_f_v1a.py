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
import os
import datetime
import msvcrt


from paho.mqtt import client as mqtt_client


broker = 'mqtt-eptm.jcloud.ik-server.com'
port = 11521
topic = "message/"
max_qos = 2

# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = ''
password = ''

messages = ''

connected = False

input_buffer = ""

def prompt():
        print("\r                                                                                                                ", end="", flush=True)
        print("\rMessage to send : " + input_buffer, end="", flush=True)

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            global messages
            messages += "\nConnected to MQTT Broker!"
            global connected
            connected = True
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        global messages
        current_date = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
        messages += f"\n[{current_date}] {msg.payload.decode()}"
        os.system("cls")
        print(messages)
        prompt()

    client.subscribe(topic, max_qos)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    client.loop_start()
    global topic
    global input_buffer
    username = input("Veuillez entrer votre nom : ")
    topic += input("Veuillez entrer le nom de votre conversation : ")
    message = input("Veuillez saisir le message de bienvenue : ")
    if message != '' :
        client.publish(topic, message, retain=True)
    
    subscribe(client)

    while True :
        if connected :
            char = msvcrt.getwche()
            if char:
                if char == "\r":
                    client.publish(topic, username + " - " + input_buffer)
                    input_buffer = ""
                elif char == "\b" :
                    input_buffer = input_buffer[:-1]
                else :
                    input_buffer += char
            prompt()
                    


if __name__ == '__main__':
    run()
