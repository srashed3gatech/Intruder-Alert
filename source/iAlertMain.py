import threading
import time
import Queue
from DBUtility import iAlertDB
from bootloader import BootLoader
''' Main entry point for the program 
    1. load realated user using db utility
    2. create bootloader with related user list and train system using images for user-id's image path and generate face_recognizer.xml
    3. generate new video file and update database with video file info
    4. start camcapture thread - pass facerecognizer.xml, new video file path and frameQ
    5. start db_framewriter thread - pass frameQ
    
    NEXT...TODO
    4. start alarm generator thread
'''

MAX_QUEUE_SIZE = 10000
DB_FRAME_WRITE_TIMEOUT_SEC = 10


faceRecogXmlFilePath = None
videoFilePath = None

#declaring queue to be used for frame exchange
frameExchangeQueue = Queue.Queue(MAX_QUEUE_SIZE)

#all threads kept track here
workerThreads = []

#asyncLock used for cases when no thread allowed to run due to some synchronization issue
# for example: bootLoader need to finish after any other thread starts
asyncLock = threading.Lock()

if __name__ == "__main__":
    db = iAlertDB()
    print "Starting bootloader ..."
    bootLoader = BootLoader(db.get_realted_users())
    modelFilePath = bootLoader.trainModel();
    
    #create a video file - name as current timestamp
    currentVideoRecFile = "./cam_cap_"+time.strftime("%Y%m%d-%H%M%S")+".avi"
    videoFileID = db.create_new_video_file(currentVideoRecFile)
    
    print "Starting cam capture ... TODO"
