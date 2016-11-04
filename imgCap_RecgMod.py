import cv2, sys, os, time
import numpy as np
from PIL import Image
import socket

################################################################################
####CONSTANTS and set up casc paths
CWD = os.getcwd()
face_cascPath = CWD+"/haarcascades/haarcascade_frontalface_alt.xml"
faceCascade = cv2.CascadeClassifier(face_cascPath)
DETECTED_IMG_DIR = CWD+"/detected_faces_imgs"
DETECTED_IMG_Path = DETECTED_IMG_DIR+"/img"
DETECTED_VD_DIR = CWD+"/detected_faces_videos"
VID = 1 ## for now, vid is not changing
DETECTED_VD_Path = DETECTED_VD_DIR+"/vid_"+str(VID)
SERVER_HOST = 'www.google.com'#'localhost'
SERVER_PORT = 80

####  set up save-to dirs
try: 
    os.makedirs(DETECTED_IMG_DIR)
except OSError:
    if not os.path.isdir(DETECTED_IMG_DIR):
        raise
try: 
    os.makedirs(DETECTED_VD_DIR)
except OSError:
    if not os.path.isdir(DETECTED_VD_DIR):
        raise
        
#### Set up the recognition model
## For face recognition we will the the LBPH Face Recognizer
recognizer = cv2.createLBPHFaceRecognizer(1,8,8,8,100.0)
recognizer.load("./face_recognizer.xml")
cv2.destroyAllWindows()
        
img_cnt = 0
frm_cnt = 0
fourcc = cv2.cv.CV_FOURCC(*'XVID')
out = cv2.VideoWriter(DETECTED_VD_Path+".avi",fourcc, 20.0, (640,480))

#### TCP connection
try:
    ## create an AF_INET, STREAM socket (TCP)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit();
try:
    remote_ip = socket.gethostbyname(SERVER_HOST)
 
except socket.gaierror:
    ## could not resolve
    print 'Hostname could not be resolved. Exiting'
    sys.exit()
 
## Connect to remote server
s.connect((remote_ip , SERVER_PORT))
print 'Socket Connected to ' + SERVER_HOST + ' on ip ' + remote_ip   


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

    messages = [];
    ## Draw a rectangle around the faces
    for (x, y, w, h) in faces:
    	roi = gray[y:y+h,x:x+w] # a face region in current frame
    	nbr_predicted, conf = recognizer.predict(roi)
    	messages.append(str(nbr_predicted)+"#"+str(conf));
    	#print "predicted label: "+str(nbr_predicted)+" conf: "+str(conf)
        if nbr_predicted>-1:
           cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        else:
           cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
        #cv2.imshow("Recognizing Face", roi)
	
    ## Display the resulting frame
    cv2.imshow('Video', frame)

    if len(faces)>0: ## save to the video file if faces are detected at this frame
	frm_cnt = frm_cnt+1    ## update frame number
	cur_time = time.time() ## get current UTC time
	out.write(frame)	## write to video buffer
	for msg in messages:
	    msg = str(VID)+"#"+str(frm_cnt)+"#"+str(cur_time)+"#"+msg
	    print "Sending msg to server: "+msg
	    try :
    	        s.sendall(msg)
	    except socket.error:
	    	#Send failed
	    	print 'Send failed'
	    	sys.exit()
	    print 'Message sent successfully'
		 
	    ## Now receive data
	    #reply = s.recv(4096) 
	    #print reply
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

## When everything is done, release the capture
out.release()
video_capture.release()
cv2.destroyAllWindows()
s.close()


