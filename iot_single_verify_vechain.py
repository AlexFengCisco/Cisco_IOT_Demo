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
    orderNo = input("Enter Order No. to verify : ")
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
        else:
            print('Order No . {} not verified , not a trust data '.format(orderNo))

    process_time = time.time() - start_time
    print("Total block chain verify time {} seconds".format(int(process_time)))
