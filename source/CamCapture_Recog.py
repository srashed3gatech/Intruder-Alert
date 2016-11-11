import threading
from classes.VideoFram import VideoFrame
import cv2, sys, os, time

'''This thread is responsible to:
        - write frame to frameRepoQ as it deletect faces from camera feed
        - write video file for recording purpose'''

class CameraCaptureNRecognition(threading.Thread):
    def __init__(self, threadID, name, 
                 videoObj, frameQueue, qLock, 
                 face_cascade_path, model_path,  
                 singleInstanceLock):
        self.videObj = videoObj
        self.frameQueue = frameQueue
        self.name = name
        self.threadID = threadID
        self.qLock = qLock
        self.face_cascPath = face_cascade_path
        self.model_path = model_path
        self.threadLock = singleInstanceLock
        
    def run(self):
        self._image_recognize()
    
    
    def _write_to_queue(self, vFrameObj):
        self.qLock.acquire()
        self.frameQueue.put(vFrameObj)
        self.qLock.release()
        
        
    def _image_recognize(self):
        self.threadLock.acquire() #ensure only one instance of this thread is running
        #### Set up the recognition model
        ## For face recognition we will the the LBPH Face Recognizer
        recognizer = cv2.createLBPHFaceRecognizer(1,8,8,8,100.0)
        recognizer.load(self.model_path)
                
        img_cnt = 0
        frm_cnt = 0
        fourcc = cv2.cv.CV_FOURCC(*'XVID')
        out = cv2.VideoWriter(self.videObj['video_path'],fourcc, 20.0, (640,480))
        
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
        
            vidFrames = VideoFrame();
            ## Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                roi = gray[y:y+h,x:x+w] # a face region in current frame
                nbr_predicted, conf = recognizer.predict(roi)
                vidFrame.confid_level = conf
                vidFrame.user_id = nbr_predicted
                vidFrame.timestamp = time.time()
                vidFrame.video_id = videoObj['video_id']
                self._write_to_queue(vidFrame)
                #print "predicted label: "+str(nbr_predicted)+" conf: "+str(conf)
                if nbr_predicted>-1:
                   cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                else:
                   cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                #cv2.imshow("Recognizing Face", roi)
            
            ## Display the resulting frame
            cv2.imshow('Video', frame)
        
            if len(faces)>0: ## save to the video file if faces are detected at this frame
                out.write(frame)    ## write to video file
                
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        ## When everything is done, release the capture
        out.release()
        video_capture.release()
        cv2.destroyAllWindows()
        s.close()
        self.threadLock.release()