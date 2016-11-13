from classes.VideoFrame import VideoFrame
import cv2, sys, os, time
from PIL import Image
import logging
import threading
import Queue
'''This thread is responsible to:
        - write frame to frameRepoQ as it deletect faces from camera feed
        - write video file for recording purpose'''

class CameraCaptureNRecognition:
    def __init__(self, videoObj, frameQueue, qLock, 
                 face_cascade_path, model_path):
        self.videoObj = videoObj
        self.frameQueue = frameQueue
        self.qLock = qLock
        self.face_cascPath = face_cascade_path
        self.model_path = model_path
        self.logger = logging.getLogger(__name__)
        
    
    
    def _write_to_queue(self, vFrameObj):
        self.qLock.acquire()
        self.frameQueue.put(vFrameObj)
        self.qLock.release()
        
        
    def _image_recognize(self):
        self.logger.info("CWD: "+os.getcwd())
        faceCascade = cv2.CascadeClassifier(self.face_cascPath)
        #### Set up the recognition model
        ## For face recognition we will the the LBPH Face Recognizer
        recognizer = cv2.createLBPHFaceRecognizer(1,8,8,8,100.0)
        self.logger.info("Openning Face cascade - "+self.model_path)
        recognizer.load(self.model_path)
                
        frm_cnt = 0
        fourcc = cv2.cv.CV_FOURCC(*'XVID')
        self.logger.info("Video Output at - %s" %self.videoObj['video_path'])
        out = cv2.VideoWriter(self.videoObj['video_path'],fourcc, 20.0, (640,480))
        videoFileId = self.videoObj["video_id"]
        
        video_capture = cv2.VideoCapture(0)
        while True:
            ## Capture frame-by-frame
            ret, frame = video_capture.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.3,
                minNeighbors=6,
                minSize=(30, 30),
                flags=cv2.cv.CV_HAAR_SCALE_IMAGE
            )
            
            frameTime = time.strftime('%Y-%m-%d %H:%M:%S')
            ## Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                roi = gray[y:y+h,x:x+w] # a face region in current frame
                nbr_predicted, conf = recognizer.predict(roi)
                
                vidFrame = VideoFrame(videoFileId, frm_cnt, 
                                      frameTime, nbr_predicted, conf);
                
                self._write_to_queue(vidFrame)
                if nbr_predicted>-1:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                else:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                #cv2.imshow("Recognizing Face", roi)
            
            ## Display the resulting frame
            cv2.imshow('Video', frame)
        
            if len(faces)>0: ## save to the video file if faces are detected at this frame
                out.write(frame)    ## write to video file
                frm_cnt += 1
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                            
        ## When everything is done, release the capture
        out.release()
        video_capture.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    CWD = os.getcwd()
    face_cascPath = CWD+"/../haarcascades/haarcascade_frontalface_alt.xml"
    faceCascade = cv2.CascadeClassifier(face_cascPath)
    DETECTED_VD_DIR = CWD+"/../Video"
    VID = time.time() ## for now, vid is not changing
    DETECTED_VD_Path = DETECTED_VD_DIR+"/vid_"+str(VID)
    MODEL_PATH = "../face_recognizer.xml"
    SERVER_HOST = 'google.com'#'localhost'
    SERVER_PORT = 80#5000
    
    videoObj = {"video_id": 1,  
                "video_path": DETECTED_VD_Path, 
                "duration_sec": -1, 
                "expiry": time.time()}
    
    obj = CameraCaptureNRecognition(videoObj, Queue.Queue(10), threading.Lock(), face_cascPath, MODEL_PATH)
    obj._image_recognize()
    
    