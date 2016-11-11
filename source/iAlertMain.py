import threading
import time
import Queue
''' Main entry point for the program 
    1. start bootloader thread and make other wait, once its done join() it
        - load realated user using db utility
        - train system using images for user-id's image path and generate face_recognizer.xml
        - generate new video file and update database with video file info
        
    2. start camcapture thread - pass facerecognizer.xml and new video file path
    
    3. start db_framewriter thread
    
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


