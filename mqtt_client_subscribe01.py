'''
   subscribe MQTT topic , consume temperature sensor value ,
   each x seconds save temperature value to txt file and compute hash

   ...upload hash result to public cloud block chain service
   save hash result and file index in local file

   from concurrent handle multi sensor clients publish message to mqtt topic
   subscribe topic and receive in a queue manner, async handle message and de-queue FIFO

'''

import os
import shutil
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
    #print(msg.topic+" "+str(msg.payload))
    message = msg.payload.decode('utf-8')
    message_queue.append(message)


if __name__=="__main__":

    global MQTT_HOST, MQTT_PORT, MQTT_TOPIC,message_queue

    MQTT_HOST= ie.MQTT_HOST
    MQTT_PORT= ie.MQTT_PORT
    MQTT_TOPIC= ie.MQTT_TOPIC
    message_queue = []
    file_queue = {}
    data_dir = './OrderData/'
    temp_dir = './temp_data/'

    mqttc=mqtt.Client()
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    try:

        mqttc.connect(MQTT_HOST,MQTT_PORT,60)
        mqttc.loop_start()

        while True:

            if message_queue:

                messge = message_queue[0]
                #print(messge)
                m_list = messge.split()
                print(m_list)
                message_queue.pop(0)
                if len(message_queue) > 0:
                    print('queue buffered length {}'.format(len(message_queue)))

                if m_list[4] == 'START':
                    file_queue[m_list[3]] = open(temp_dir+m_list[3],'a')
                    print(file_queue)

                if file_queue and m_list[4]!= 'START' and m_list[4]!= 'STOP':
                    file_queue[m_list[3]].write('{} {} {}'.format(m_list[0],m_list[1],m_list[4]+'\n'))

                if m_list[4] == 'STOP':
                    file_queue[m_list[3]].close()
                    shutil.move(temp_dir+m_list[3],data_dir+m_list[3])
                    file_queue.pop(m_list[3])
                    print(file_queue)

            #time.sleep(3)


    except Exception as e:
            print("Programm interrupted")
            print(e)
            mqttc.loop_stop()
            mqttc.disconnect()
