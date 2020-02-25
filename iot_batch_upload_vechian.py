'''

  TODO think about multi thread upload data hash to vechain

  TODO deploy SQL lite for local kv and status store with status lock/unlock

'''
import os
import hashlib
import json
import pprint as pp
import iot_env as ie
import vechain as VC
import time
# List all files in a directory using os.listdir
data_path = ie.data_dir
vidListNo = 1

if __name__ == "__main__":

    while True:
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
        for orderNo in os.listdir(data_path):
            if os.path.isfile(os.path.join(data_path, orderNo)):


                if not orderNo in order_vid:
                    print("uploading Order No. {} data hash...".format(orderNo))
                    # create uid for sub account
                    uid = vc.create_sub_acc(orderNo, "sensor") # sensor as sub account
                    print("uid = {}".format(uid))

                    # generate vid list for request No.
                    vid_lists = vc.gen_vid(orderNo, vidListNo)
                    pp.pprint(vid_lists)

                    # generate file data hash
                    f = open(data_path+orderNo)
                    content = f.read()
                    m = hashlib.sha256()
                    m.update(content.encode('utf-8'))
                    data_hash = '0x'+ m.hexdigest()
                    print('hash result is {}'.format(data_hash))
                    f.close()

                    # upload data hash pair with  vid for request No . with uid

                    txlist = vc.upload_hash_blockchain(data_hash, vid_lists, orderNo, uid)
                    pp.pprint(txlist)
                    order_vid[orderNo] = vid_lists[0]

        process_time = time.time() - start_time
        pp.pprint(order_vid)

        kv_file = open("iot_order_vid", 'w')
        kv_file.write(json.dumps(order_vid))
        kv_file.close()

        print("Total upload to chain time {} seconds".format(int(process_time)))

        time.sleep(ie.iot_batch_upload_interval)


