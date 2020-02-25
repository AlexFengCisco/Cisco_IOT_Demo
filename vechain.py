'''
   vechain class Rest API

   memo : when create or generate sth , seems needs quite a lont time , just wait for data status = SUCCESS and go on

   for same requestNo , get same vidList and get same uid

   Occupy vidlist was tested failed , message was success , and status was success but lists both sucessList and failureList were empty!!!

   Dec 2019

   By Alex Feng

'''
import time
import hashlib
import random
import requests
import vechian_env as ve


class VeChain():
    '''
    Class for vechainn Rest API
    Generate API token
    Create sub account
    Generate vid List
    upload data hash
    query data hash
    '''

    def __init__(self):
        '''
        Constructor

        '''
        self.token_url = ve.base_url + ve.token_url
        self.create_sub_acc_url = ve.base_url + ve.create_sub_account_url
        self.gen_vidlist_url = ve.base_url + ve.gen_vid_url
        self.occ_vidlist_url = ve.base_url + ve.occ_vids_url
        self.upload_hash_url = ve.base_url + ve.upload_hash_blockchain_url
        self.query_lastest_hash_url = ve.base_url + ve.query_latest_hash_url
        self.token = self.get_token(ve.developer_id,ve.developer_key)


    def gen_get_token_payload(self,developer_id, developer_key):
        '''
        Generate token digest sha256
        :param developer_id:
        :param developer_key:
        :return:
        '''
        digits = ''
        d_id = 'appid={}&'.format(developer_id)
        d_key = 'appkey={}&'.format(developer_key)
        timestamp = str(int(time.time()))
        timestamp_hash = 'timestamp={}'.format(timestamp)
        nonce = digits.join(random.sample('12345678901234567890', 16)).replace(' ', '')
        nonce_hash = 'nonce={}&'.format(nonce)

        sign = d_id + d_key + nonce_hash + timestamp_hash
        signature_hash = hashlib.sha256()
        signature_hash.update(sign.encode('utf-8'))
        signature = signature_hash.hexdigest()

        payload = '''{
        "appid": "%s",
        "nonce": "%s",
        "signature": "%s",
        "timestamp": "%s",
        "source": "%s"
        }''' % (developer_id, nonce, signature, timestamp,nonce)
        return payload


    def get_token(self, developer_id, developer_key):
        print("=" * 20 + " Get Develop Token " + "=" * 20)
        '''
        post to get token
        :param url:
        :param developer_id:
        :param developer_key:
        :return:
        '''
        url = self.token_url
        headers = {'Content-Type': "application/json"}
        get_token_payload = self.gen_get_token_payload(developer_id, developer_key)
        print(get_token_payload)
        try:
            response = requests.request("POST", url, data=get_token_payload, headers=headers).json()
            print(response)

            if response['message'] == 'success':
                token = response['data']['token']

        except Exception as e:
            print('ERROR get token')
            print(e)
        return token


    def gen_vid(self,requestNo, quantity):
        token = self.token
        print("=" * 20 + " Generate Vid List " + "=" * 20)
        '''
        Generate vid list with
        :param url:
        :param token:
        :param requestNo:
        :param quantity:
        :return:
        '''

        url = self.gen_vidlist_url
        vid_list = []
        headers = {
            'Content-Type': "application/json",
            'x-api-token': token
        }
        payload = '''{"requestNo":"%s",       
                       "quantity":%s}''' % (requestNo, str(quantity))

        print(headers)
        print(payload)

        while True:
            try:
                response = requests.request("POST", url, data=payload, headers=headers).json()
                print(response)
                if response['message'] == 'success' and response["data"]["status"] == "SUCCESS":
                    vid_list = response["data"]["vidList"]

            except Exception as e:
                print('ERROR get vid list')
                print(e)
            '''
              test result , not very stable , sometimes response content is 'generating ....' and sometimes error exception thrown 
              {'data': None, 'code': 1003, 'message': 'Exception, parameter  is illegal'}
    
            '''
            if response['message'] == 'success' and response["data"]["status"] == "SUCCESS":
                break
            time.sleep(10)

        return vid_list


    def occ_vids(self,requestNo, vidList):  #### ignore
        token = self.token
        print("=" * 20 + " Occupy vid list " + "=" * 20)

        url = self.occ_vidlist_url
        success_list = []
        failure_list = []
        headers = {
            'Content-Type': "application/json",
            'x-api-token': token
        }

        payload = '''{"requestNo": "%s","vidList": ["0X5347CAF7FAA82A6298EE1AB913D81945FABCB3FC9709B0723E213E2A4B66B1F5", "0X81BDA6456AF7F9010B9BFEF6F6A3F50F6C5AE364EFEF4EC5EB141FB86D129C38", "0X3F6ADF36A72355F047444997389B70871EE39EEC83F3FCDAEB0D4693594156B1", "0X6CB4F18B5AD58BE8B59A153461E2D4A4044FD7A9A506F9ADBF48914D8786E2A5"]}''' % (
            requestNo)

        print(headers)
        print(payload)

        try:
            response = requests.request("POST", url, data=payload, headers=headers).json()
            print(response)
            if response['message'] == 'success':
                success_list = response["data"]["successList"]
                failure_list = response["data"]["failureList"]

        except Exception as e:
            print('ERROR occ vids')
            print(e)
        return success_list, failure_list


    def create_sub_acc(self,requestNo, sub_acc):
        print("=" * 20 + " Create sub account " + "=" * 20)
        token = self.token
        url = self.create_sub_acc_url
        headers = {
            'Content-Type': "application/json",
            'x-api-token': token
        }
        payload = '''{"requestNo":"%s", "name":"%s"}''' % (requestNo, sub_acc)
        print(headers)
        print(payload)

        while True:
            try:
                response = requests.request("POST", url, data=payload, headers=headers).json()
                print(response)
                if response['message'] == 'success' and response["data"]["status"] == 'SUCCESS':
                    uid = response["data"]["uid"]


            except Exception as e:
                print('ERROR create sub account')

                print(e)

            if response['message'] == 'success' and response["data"]["status"] == "SUCCESS":
                break
            time.sleep(10)

        return uid


    def upload_hash_blockchain(self,data_hash, vidList, requestNo, uid):
        print("=" * 20 + " Upload data hash to block chain " + "=" * 20)
        token = self.token
        url = self.upload_hash_url
        txList = []
        headers = {
            'Content-Type': "application/json",
            'x-api-token': token
        }

        payload = '''
    {"data": [{"dataHash":"%s",
               "vid":"%s"}],
     "requestNo": "%s",
     "uid":"%s"
    }
    ''' % (data_hash, vidList[0], requestNo, uid)

        print(headers)
        print(payload)

        while True:
            try:
                response = requests.request("POST", url, data=payload, headers=headers).json()
                print(response)
                if response['message'] == 'success' and response["data"]["status"] == 'SUCCESS':
                    txList = response['data']['txList']


            except Exception as e:
                print('ERROR upload data_hash ')
                print(e)
            if response['message'] == 'success' and response["data"]["status"] == "SUCCESS":
                break
            time.sleep(10)

        return txList


    def query_latest_hash(self,vid):
        print("=" * 20 + "Query the lastest data hash from blockchain" + "=" * 20)
        token = self.token
        url = self.query_lastest_hash_url
        data_hash = ''
        headers = {
            'Content-Type': "application/json",
            'x-api-token': token
        }

        payload = '''{"vid":"%s"}''' % vid[0]
        try:
            response = requests.request("POST", url, data=payload, headers=headers).json()
            print(response)
            if response['message'] == 'success':
                data_hash = response["data"]["dataHash"]
                pass


        except Exception as e:
            print('ERROR upload data_hash ')
            print(e)

        return data_hash






