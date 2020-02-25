'''
   simulator send temperature sensor random value to MQTT
   temp value range 0-30\

   combine with wen rest api, read API flag and orderNo,start and stop sending sensor message to mqtt topic

   get status from central server REST API, each interval once.
   and base on response , send order No. start and stop


'''

import time
import paho.mqtt.client as mqtt
from datetime import datetime
from random import randint
import json
import requests
import iot_env as ie



if __name__=="__main__":

    global MQTT_HOST,MQTT_PORT,MQTT_TOPIC,voiceDb

    MQTT_HOST=ie.MQTT_HOST
    MQTT_PORT=ie.MQTT_PORT
    MQTT_TOPIC=ie.MQTT_TOPIC

    iot_base_url = ie.REST_API_BASE_URL
    sensor_id = ie.sensor_id
    message_interval = ie.message_interval

    iot_control_url = iot_base_url+"sensorstatus"
    iot_control_payload = '''{ "sensor_id": "%s"}'''%sensor_id
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    mqttc=mqtt.Client()
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
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                temp_value = randint(0,40)
                if status == "STOPPED" and flag == 'START':
                    mqttc.publish(MQTT_TOPIC, '{} {} {} {}'.format(dt_string, sensor_id, order_No, flag))
                    status = "SENDING"
                if status == "SENDING":
                    mqttc.publish(MQTT_TOPIC,'{} {} {} {}'.format(dt_string,sensor_id,order_No,str(temp_value)))

                if status == "SENDING" and flag == "STOP":
                    mqttc.publish(MQTT_TOPIC,'{} {} {} {}'.format(dt_string,sensor_id,order_No,flag))
                    status = "STOPPED"
                time.sleep(message_interval)
            except Exception as fe:
                print(fe)
                time.sleep(message_interval)
    except Exception as e:
            print("Interrupted")
            print(e)
            mqttc.loop_stop()
            mqttc.disconnect()


