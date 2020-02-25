'''
  Demo vechian rest api class
'''
import vechain as VC
import time
import pprint as pp

if __name__ == "__main__":
    requestNo = 10
    vidListNo = 1

    vc = VC.VeChain()

    #create uid for sub account
    uid = vc.create_sub_acc(requestNo, "sensor")
    print("uid = {}".format(uid))

    #generate vid list for request No.
    vid_lists = vc.gen_vid(requestNo, vidListNo)
    pp.pprint(vid_lists)


    data_hash = "0x1010aaee5a07861f94fe272ad21f223197d94aea08eb65cf34c2c88600ffff99"  #test data hash

    start_time = time.time()

    #upload data hash pair with  vid for request No . with uid
    txlist = vc.upload_hash_blockchain(data_hash, vid_lists, requestNo, uid)
    pp.pprint(txlist)

    #query data hash with vid
    data_hash = vc.query_latest_hash(vid_lists)
    print("Query the lastest hased data = {} ".format(data_hash))

    process_time = time.time() - start_time
    print("Total upload to chain and query time {} seconds".format(int(process_time)))


