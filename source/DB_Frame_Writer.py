import threading
from DBUtility import iAlertDB
from classes.VideoFrame import VideoFrame
import logging
import time

'''This thread is responsible to write frame from frameRepoQ into database'''

class DBFrameWriter(threading.Thread):
    def __init__(self, threadID, name, 
                 frameQ, frameQLock, 
                 polling_interval_sec, exitThreadFlag,
                 db_instance):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.frameQ = frameQ
        self.qLock = frameQLock
        self.exitThreadFlag = exitThreadFlag
        self.polling_interval_sec = polling_interval_sec
        self.db_instance = db_instance
        self.logger = logging.getLogger(__name__)
    
    def run(self):
        self.logger.info("Starting DBFrameWriter...")
        while not self.exitThreadFlag:
            vFrames = self._readQFrames()
            if(len(vFrames) > 0):
                self.logger.info("Writing Frames")
                self._writeFrameToDB(vFrames)
            self.logger.info("going to sleep for %s" %(self.polling_interval_sec))
            time.sleep(self.polling_interval_sec)
        self.logger.info("Exiting DBFrameWriter...")    
        
    def _readQFrames(self):
        vframeList = []
        self.qLock.acquire()
        while not self.frameQ.empty():
            vframeList.append(self.frameQ.get())
        self.qLock.release()
        return vframeList
        
    def _writeFrameToDB(self, vFrames):
        self.db_instance.insert_frames(vFrames)
        self.logger.info("All frame written...")