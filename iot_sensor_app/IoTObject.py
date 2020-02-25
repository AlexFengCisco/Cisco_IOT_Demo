#coding:UTF-8
import json,uuid
import platform,time,random
from datetime import datetime

STATE_NORMAL="Normal"
STATE_DANGER="Warning"
STATE_ALTER="Alert"

LATI_LO=12.97
LATI_HI=13.20

LONGI_LO=77.59
LONGI_HI=79.26


import socket
import fcntl
import struct

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])



class IoTObject(object):

    def __init__(self):
        self.threshHold=30
        self.down_threshold=10
        self.up_threshold=100
        self.locations=["001","002","003","004","005"]
       
        self.nodeName=platform.node()

        self.deviceType=None
        self.deviceName=None
        self.state=STATE_NORMAL
        self.metricFlag='cm'
        self.value=-999
        self.longitude=round(float(random.uniform(LATI_LO, LATI_HI)),2)
        self.latitude=round(float(random.uniform(LATI_LO, LATI_HI)),2)

    def Set_Data(self,d):
        self.value=d

    def Get_Location(self):
         return self.locations[random.randint(0,3)]

    def Get_TimeStamp(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def Get_EventId(self):
        return str(uuid.uuid4())

    def Get_State(self,v):
        pass

    def Get_Msg(self):
        pass

    def Get_Data(self):
        return self.value
        pass

    def Get_Longitude(self):
        return round(float(random.uniform(LATI_LO, LATI_HI)),2)


    def Get_latitude(self):
        return round(float(random.uniform(LATI_LO, LATI_HI)),2)

    def ToJson(self):
        _d=dict()
        _d["MetricFlag"]=self.metricFlag
        _d["DeviceHost"]=self.nodeName
        _d["DeviceName"]=self.deviceName
        _d["DeviceType"]=self.deviceType
        _d["MetricFlag"]=self.metricFlag
        _d["Location"]=self.Get_Location()
        _d["TimeStamp"]=self.Get_TimeStamp()
        _d["EventId"]=self.Get_EventId()
        _val=self.Get_Data()
        _d["Data"]=_val
        _d["State"]=self.Get_State(_val)
        _d["Msg"]=self.Get_Msg()
        _d["Latitude"]=self.Get_latitude()
        _d["Longitude"]=self.Get_Longitude()
        return json.dumps(_d, ensure_ascii=False)
