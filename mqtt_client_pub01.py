'''
   simulator send temperature sensor random value to MQTT

   temp value range 0-30

'''

import time
import paho.mqtt.client as mqtt
from datetime import datetime
from random import randint



if __name__=="__main__":

    global MQTT_HOST,MQTT_PORT,MQTT_TOPIC,voiceDb

    MQTT_HOST='10.75.58.26'
    MQTT_PORT=1883
    MQTT_TOPIC="sensor"
    sensor_id = "01"
    order_No = "0018"
    message_interval = 10
    message_count = 10

    mqttc=mqtt.Client()
    try:
       mqttc.connect(MQTT_HOST,MQTT_PORT,60)
       mqttc.loop_start()
       flag = "START"
       '''
         flag START
              SENDING
              STOP
       '''
       count = 0
       while True:
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            temp_value = randint(0,40)
            if flag == 'START':
                mqttc.publish(MQTT_TOPIC, '{} {} {} {}'.format(dt_string, sensor_id, order_No, flag))
                flag = "SENDING"
            else:
                mqttc.publish(MQTT_TOPIC,'{} {} {} {}'.format(dt_string,sensor_id,order_No,str(temp_value)))
            count +=1
            if count > message_count:
                flag = "STOP"
                mqttc.publish(MQTT_TOPIC,'{} {} {} {}'.format(dt_string,sensor_id,order_No,flag))
                mqttc.loop_stop()
                mqttc.disconnect()
                break
            time.sleep(message_interval)
    except Exception as e:
            print("Interrupted")
            print(e)
            mqttc.loop_stop()
            mqttc.disconnect()


