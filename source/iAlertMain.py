import threading
import time
import Queue
import os
from DBUtility import iAlertDB
from bootloader import BootLoader
from CamCapture_Recog import CameraCaptureNRecognition
from DB_Frame_Writer import DBFrameWriter
import logging
''' Main entry point for the program 
    1. load realated user using db utility
    2. create bootloader with related user list and train system using images for user-id's image path and generate face_recognizer.xml
    3. generate new video file and update database with video file info
    4. start camcapture thread - pass facerecognizer.xml, new video file path and frameQ
    5. start db_framewriter thread - pass frameQ
    
    NEXT...TODO
    4. start alarm generator thread
    *****Deal with confidence thresholds of each user: cannot have diff threshold for each user unless split to diff xml*****
'''

MAX_QUEUE_SIZE = 10000
DB_FRAME_WRITE_TIMEOUT_SEC = 10

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

faceRecogXmlFilePath = None
videoFilePath = None
face_cascade_path = "../haarcascades/haarcascade_frontalface_alt.xml" 

#declaring queue to be used for frame exchange
frameExchangeQueue = Queue.Queue(MAX_QUEUE_SIZE)
qLock = threading.Lock()
#all threads kept track here
workerThreads = []
threadID = 1
#asyncLock used for cases when no thread allowed to run due to some synchronization issue
# for example: bootLoader need to finish after any other thread starts
singleCameraCaptureLock = threading.Lock()
stopDBWriterThreadFlag = False

if __name__ == "__main__":
    db = iAlertDB()
    logger.info("Starting bootloader ...")
    bootLoader = BootLoader(db.get_realted_users())
    faceRecogXmlFilePath = bootLoader.trainModel()
    
    #create the folder of Video is not existed
    try: 
        os.makedirs("../Video/")
    except OSError:
        if not os.path.isdir("../Video/"):
            raise
    #create a video file - name as current timestamp
    currentVideoRecFile = "../Video/cam_cap_"+time.strftime("%Y%m%d-%H%M%S")+".avi"
    videoObject = db.create_new_video_file(currentVideoRecFile)
    
    camCapThread = CameraCaptureNRecognition(videoObject, frameExchangeQueue, qLock, 
                 face_cascade_path, faceRecogXmlFilePath)
    
    logger.info("Starting frame db writer ...")
    dbWriterThread = DBFrameWriter(threadID, "DB_Frame_Writer", 
                 frameExchangeQueue, qLock, 
                 DB_FRAME_WRITE_TIMEOUT_SEC, stopDBWriterThreadFlag,
                 db)
    workerThreads.append(dbWriterThread)
    dbWriterThread.start()
    camCapThread._image_recognize() #this doesn't work if its a thread
    #camCapThread.old_function()
    
    while not frameExchangeQueue.empty():
        pass
    #camera capture closed, now signal for dbwriter close and close the program
    stopDBWriterThreadFlag = True
    
    for t in workerThreads:
        t.join()

