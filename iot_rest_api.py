'''
  IOT restful API , for IOT control message

@author: AlexFeng
'''


import time
import pprint as pp
import os
import hashlib
import paho.mqtt.client as mqtt
from datetime import datetime
from random import randint
from flask import Flask, render_template, Response, request, redirect, url_for
#from flask import request
import json
import vechain as VC
import iot_env as ie

iot_file = './iot_control.cfg'
app = Flask(__name__)
data_path = ie.data_dir
vidListNo = 1

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/forward/", methods=['POST'])
def move_forward():
    #Moving forward code
    forward_message = "Moving Forward..."
    return render_template('index.html', message=forward_message);

@app.route('/sensorstatus', methods=['POST'])
def sensor_status():
    print(request.json)
    if not request.json or not request.json['sensor_id']:
        return ('''{"error_msg":"ERROR body, enpty or missing sensor id..."}''')
    else:

        try:
            with open(iot_file, 'r') as f:

                controls = json.load(f)
                #print(controls)
                control = controls[request.json["sensor_id"]]
                print(control)
                # f.write(json.dumps(control))
        except Exception as e:
            control = {}
            print(e)

    return control

@app.route('/sensorcontrol', methods=['POST'])
def sensor_control():
    print(request.json['control']['flag'])
    if not request.json or not request.json['control']:
        return ('''{"error_msg":"ERROR body, enpty or missing flag..."}''')
    else:
        task = json.dumps(request.json)
        print(request.json)
        try:
            with open(iot_file,'r') as f:

                controls = json.load(f)
                print(controls)
                controls[request.json["sensor_id"]] = request.json['control']
                print(controls)
                #f.write(json.dumps(control))
        except Exception as e:
            controls = {}
            print(e)
        with open(iot_file,'w') as f:
            controls[request.json["sensor_id"]] = request.json['control']
            f.write(json.dumps(controls))

    return task

@app.route('/batchblockchaincheck',methods = ['GET'])
def batch_blockchain_check():

    try:
        kv_file = open("iot_order_vid", 'r')
        order_vid_content = kv_file.read()
        if order_vid_content:
            order_vid = json.loads(order_vid_content)
            pp.pprint(order_vid)
        else:
            order_vid = {}
    except Exception as e:
        print(e)
        order_vid = {}

    start_time = time.time()

    vc = VC.VeChain()

    return_result = {}
    return_result["result"] = []
    for orderNo in os.listdir(data_path):
        check_result = {}
        if os.path.isfile(os.path.join(data_path, orderNo)):

            if not orderNo in order_vid:
                print("Order data hash has not been uploaded to vechain ,verify later ...... ".format(orderNo))
            else:

                # generate file data hash
                f = open(data_path + orderNo)
                content = f.read()
                m = hashlib.sha256()
                m.update(content.encode('utf-8'))
                data_hash = '0x' + m.hexdigest()
                print('hash result is {}'.format(data_hash))
                f.close()

                # upload data hash pair with  vid for request No . with uid
                print('vid is {}'.format(order_vid[orderNo]))
                vid_lists = [order_vid[orderNo]]
                data_hash_vechain = vc.query_latest_hash(vid_lists)
                pp.pprint(data_hash_vechain)
                if data_hash == data_hash_vechain:
                    print('Order No . {} verified ,trust it ...'.format(orderNo))
                    check_result["orderNo"] = orderNo
                    check_result["status"] = "Blockchain Verified"
                else:
                    print('Order No . {} not verified , not a trust data '.format(orderNo))
                    check_result["orderNo"] = orderNo
                    check_result["status"] = "Blockchain NOT Verified, data changed"
        return_result["result"].append(check_result)

    process_time = time.time() - start_time
    print("Total block chain verify time {} seconds".format(int(process_time)))

    return_result["total_time"] = int(process_time)
    return return_result


@app.route('/singleblockchaincheck',methods = ['POST'])
def single_blockchain_check():
    orderNo = request.json['orderNo']
    try:
        kv_file = open("iot_order_vid", 'r')
        order_vid_content = kv_file.read()
        if order_vid_content:
            order_vid = json.loads(order_vid_content)
            pp.pprint(order_vid)
        else:
            order_vid = {}
    except Exception as e:
        print(e)
        order_vid = {}

    start_time = time.time()

    vc = VC.VeChain()

    if not orderNo in order_vid:
        print("Order data hash has not been uploaded to vechain ,verify later ...... ".format(orderNo))
        return_result ='''{"status":"Waitting"}'''
    else:

        # generate file data hash
        f = open(data_path + orderNo)
        content = f.read()
        m = hashlib.sha256()
        m.update(content.encode('utf-8'))
        data_hash = '0x' + m.hexdigest()
        print('hash result is {}'.format(data_hash))
        f.close()

        # upload data hash pair with  vid for request No . with uid
        print('vid is {}'.format(order_vid[orderNo]))
        vid_lists = [order_vid[orderNo]]
        data_hash_vechain = vc.query_latest_hash(vid_lists)
        pp.pprint(data_hash_vechain)
        if data_hash == data_hash_vechain:
            print('Order No . {} verified ,trust it ...'.format(orderNo))

            with open(data_path+orderNo) as of:
                content = of.read().splitlines()
                content_list = []
                for line in content:
                    content_list.append(line.split())


            return_result = '''{"status":"Verified","orderData":"%s"}'''%str(content)
            print(return_result)
        else:
            print('Order No . {} not verified , not a trust data '.format(orderNo))
            return_result = '''{"status":"Failed , Data changed!!"}'''

    process_time = time.time() - start_time
    print("Total block chain verify time {} seconds".format(int(process_time)))

    return json.loads(return_result)

if __name__=="__main__":

    print("starting web rest api service ")
    app.run(host = '0.0.0.0')




