from __future__ import print_function
from __future__ import division
import serial
import time
import threading
import signal
import os
import json
import requests
import struct
import binascii
from datetime import datetime
import paho.mqtt.client as mqtt


s_output = ''
g_output = ''

#sdev = serial.Serial(port="/dev/tty.USA19H14414P1.1", baudrate=9600)
sdev = serial.Serial(port="/dev/ttyS1", baudrate=9600)
sdev.bytesize = serial.EIGHTBITS  # number of bits per bytes
sdev.parity = serial.PARITY_NONE  # set parity check: no parity
sdev.stopbits = serial.STOPBITS_ONE  # number of stop bits
sdev.timeout = 5

sdev1 = serial.Serial(port="/dev/ttyS4", baudrate=9600)
sdev1.bytesize = serial.EIGHTBITS  # number of bits per bytes
sdev1.parity = serial.PARITY_NONE  # set parity check: no parity
sdev1.stopbits = serial.STOPBITS_ONE  # number of stop bits
sdev1.timeout = 5


ask = b'\x01\x03\x00\x00\x00\x02\xc4\x0b'

def _sleep_handler(signum, frame):
    print("SIGINT Received. Stopping CAF")
    raise KeyboardInterrupt

def _stop_handler(signum, frame):
    print("SIGTERM Received. Stopping CAF")
    raise KeyboardInterrupt

signal.signal(signal.SIGTERM, _stop_handler)
signal.signal(signal.SIGINT, _sleep_handler)


def on_connect(mosq, obj, rc):
    print("rc: " + str(rc))

def on_message(mosq, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def on_publish(mosq, obj, mid):

    pass # to avoid print on iot console

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mosq, obj, level, string):
    print(string)


def send(str):
    sdev.write((str+'\r\n').encode('utf-8'))
    #time.sleep(0.1)

class SerialThread(threading.Thread):
    def __init__(self):
        super(SerialThread, self).__init__()
        self.name = "SerialThread"
        self.setDaemon(True)
        self.stop_event = threading.Event()



    def stop(self):
        self.stop_event.set()

    def run(self):
        global s_output
        while True:
            sdev.write(ask)
            time.sleep(0.5)
            if self.stop_event.is_set():
                break
            while sdev.inWaiting() > 0:
                s_output = sdev.read(9)


                #print(type(s_output))
                #print(len(s_output))
                #print(s_output)
                str_return_data = s_output.encode('hex')
                #print(str_return_data[-8:-4])
                feedback_data = int(str_return_data[-8:-4], 16)/10
                print("Temperature is "+str(feedback_data))
                #print(s_output.decode('hex'))

                #print(time.time())
                time.sleep(0.1)
        sdev.close()

class GpsThread(threading.Thread):
    def __init__(self):
        super(GpsThread, self).__init__()
        self.name = "GpsThread"
        self.setDaemon(True)
        self.stop_event = threading.Event()


    def stop(self):
        self.stop_event.set()

    def run(self):
        global g_output
        while True:
            #sdev.write(ask)
            #time.sleep(0.5)
            if self.stop_event.is_set():
                break
            while sdev1.inWaiting() > 0:
                gps_output = sdev1.readline()
                print(gps_output)
                if '$GPRMC' in gps_output:
                    g_output = gps_output
                    print(g_output)

                time.sleep(0.1)
        sdev1.close()


if __name__=="__main__":
    fsm = 'init'
    ter_line = ''
    s = SerialThread()
    s.start()
    g = GpsThread()
    g.start()
    _val1 = ''


    MQTT_HOST= "192.168.1.100"
    MQTT_PORT= 1883
    MQTT_TOPIC_VOICE= "sensor"
    sensor_id = "IR809"
    message_interval = 2

    REST_API_HOST = "http://192.168.1.10:5000/"


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
                #_val1=voiceDb.Get_Data()
                #print(flag)
                #print(order_No)
                #print(_val1)
                #_val1 = randint(0,40)
                #if not s_output == _val1:
                #sdev.write(ask)
                time.sleep(1)

                str_return_data = s_output.encode('hex')
                #print(str_return_data[-8:-4])
                feedback_data = int(str_return_data[-8:-4], 16)/10
                #print(feedback_data)
                _val1 = str(feedback_data)
                if g_output:
                    gl = g_output.split(',')
                    # gps_info = gl[3]+gl[4]+'/'+gl[5]+gl[6]
                    gps_info = str(float(gl[3])/100)+gl[4]+'/'+str(float(gl[5])/100)+gl[6]
                else:
                    gps_info = 'GpsLost'
                #_val1 = sensors[0]
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                if status == "STOPPED" and flag == "START":
                    mqttc.publish(MQTT_TOPIC_VOICE, '{} {} {} {}'.format(dt_string, sensor_id, order_No, flag))
                    status = "SENDING"
                if status == "SENDING":
                    message = '{} {} {} {}'.format(dt_string, sensor_id, order_No, gps_info+','+_val1)
                    mqttc.publish(MQTT_TOPIC_VOICE,message)
                    print(message)
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
