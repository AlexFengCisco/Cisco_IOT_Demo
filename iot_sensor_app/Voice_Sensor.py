#coding:UTF-8
from IoTObject import IoTObject,STATE_DANGER ,STATE_NORMAL ,STATE_ALTER,get_ip_address
import time
import grovepi
from grove_rgb_lcd import *
class Voice_GateWay_Helper(IoTObject):


    def __init__(self):
        IoTObject.__init__(self)
        self.deviceName="Noise Sensor"
        self.deviceType="Noise"
        self.metricFlag="dB"
        self.up_threshold=80
        self.down_threshold=50
        self.pin=0
        grovepi.pinMode(self.pin,"INPUT")

        setRGB(0,128,64)

    def Get_State(self,v):
        if float(v)>float(self.up_threshold):
           self.state=STATE_DANGER
           return STATE_DANGER
        elif(float(v)>float(self.down_threshold) and (float(v)<float(self.up_threshold))):
           self.state=STATE_ALTER
           return STATE_ALTER
        else:
           self.state=STATE_NORMAL
           return STATE_NORMAL


    def Get_Location(self):
         return self.locations[0]


    def Get_Data(self):
        import math
        sensor_value = grovepi.temp(0,'1.2')
        sensor_value = round (sensor_value,2)
        
        setText(get_ip_address('eth0')+"\nTemp is:"+str(sensor_value)+"C\n")
        return sensor_value



