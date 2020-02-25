#coding:UTF-8
import os
import time
from datetime import datetime
import paho.mqtt.client as mqtt
import sys
from iot_sensor_app.Voice_Sensor import Voice_GateWay_Helper
from iot_sensor_app.IoTObject import get_ip_address
from iot_sensor_app.grove_rgb_lcd import *
import requests
import json
import iot_env as ie

#reload(sys)
sys.setdefaultencoding('utf-8')

def on_connect(mosq, obj, rc):
    print("rc: " + str(rc))

def on_message(mosq, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def on_publish(mosq, obj, mid):
    #print("mid: " + str(mid))
    pass # to avoid print on iot console

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mosq, obj, level, string):
    print(string)


if __name__=="__main__":

    global MQTT_HOST,MQTT_PORT,MQTT_TOPIC,voiceDb
    voiceDb=Voice_GateWay_Helper()
    MQTT_HOST= ie.MQTT_HOST
    MQTT_PORT= ie.MQTT_PORT
    MQTT_TOPIC_VOICE= ie.MQTT_TOPIC
    sensor_id = ie.sensor_id
    message_interval = ie.message_interval

    REST_API_HOST = ie.REST_API_BASE_URL
    #message_count = 30
    
    iot_control_url = REST_API_HOST+"sensorstatus"
    iot_control_payload = '''{ "sensor_id": "%s"}'''%sensor_id
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    mqttc=mqtt.Client()
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe
    try:
       mqttc.connect(MQTT_HOST,MQTT_PORT,60)
       mqttc.loop_start()
       status = "STOPPED"
       
       while True:
            try:
                response = requests.request("POST", iot_control_url, headers=headers, data=iot_control_payload)
                control = json.loads(response.text)
                flag = control["flag"]
                order_No = control["orderNo"] 
                _val1=voiceDb.Get_Data()
                #print(flag)
                #print(order_No)
                #print(_val1)
                now = datetime.now()
	        dt_string = now.strftime("%d/%m/%Y %H:%M:%S") 
                if status == "STOPPED" and flag == "START":
                    mqttc.publish(MQTT_TOPIC_VOICE, '{} {} {} {}'.format(dt_string, sensor_id, order_No, flag))
                    status = "SENDING"
                if status == "SENDING":
                    message = '{} {} {} {}'.format(dt_string, sensor_id, order_No, _val1)  
                    mqttc.publish(MQTT_TOPIC_VOICE,message)
                if status == "SENDING" and flag == "STOP":
                    status = "STOPPED"
                    mqttc.publish(MQTT_TOPIC_VOICE,'{} {} {} {}'.format(dt_string,sensor_id,order_No,flag))
                time.sleep(message_interval)
            except Exception as ef:
                print(ef)
                time.sleep(message_interval)
    except Exception as e:
            print("Programm interrupted")
            print(e)
            mqttc.loop_stop()
            mqttc.disconnect()



