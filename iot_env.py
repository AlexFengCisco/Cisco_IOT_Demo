# IOT control Server enviroment
MQTT_HOST = '192.168.1.100'
MQTT_PORT = 1883
MQTT_TOPIC = "sensor"


REST_API_BASE_URL = "http://127.0.0.1:5000/"

data_dir = './OrderData/'
temp_dir = './temp_data'

iot_batch_upload_interval = 120 # back end check file update and upload to chain time interval


# IOT mqtt Client enviroment



sensor_id = "IOT_Simulator"
message_interval = 10
#message_count = 10

#iot_control_url = "http://127.0.0.1:5000/sensorstatus"
#iot_control_payload = '''{ "sensor_id": "%s"}'''%sensor_id
#iot_control_headers = {
#    'Accept': 'application/json',
#    'Content-Type': 'application/json'
#}