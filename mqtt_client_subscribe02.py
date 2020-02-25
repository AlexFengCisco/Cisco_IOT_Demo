'''
   subscribe MQTT topic , consume temperature sensor value ,
   each x seconds save temperature value to txt file and compute hash

   ...upload hash result to public cloud block chain service
   save hash result and file index in local file

   from concurrent handle multi sensor clients publish message to mqtt topic
   subscribe topic and receive in a queue manner, async handle message and de-queue FIFO

'''

import os
import hashlib
import time
import paho.mqtt.client as mqtt
from datetime import datetime
import iot_env as ie



def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_TOPIC)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global message_queue
    print(msg.topic+" "+str(msg.payload))
    #message = msg.payload.decode('utf-8')
    #message_queue.append(message)


if __name__=="__main__":

    global MQTT_HOST, MQTT_PORT, MQTT_TOPIC,message_queue

    MQTT_HOST = ie.MQTT_HOST
    MQTT_PORT= ie.MQTT_PORT
    MQTT_TOPIC= ie.MQTT_TOPIC
    message_queue = []
    file_queue = {}
    #data_dir = './OrderData/'

    mqttc=mqtt.Client()
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    try:

        mqttc.connect(MQTT_HOST,MQTT_PORT,60)
        mqttc.loop_start()

        while True:

            pass

            #time.sleep(3)


    except Exception as e:
            print("Programm interrupted")
            print(e)
            mqttc.loop_stop()
            mqttc.disconnect()
