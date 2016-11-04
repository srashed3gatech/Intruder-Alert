import cv2, sys, os, time
import numpy as np
from PIL import Image
import socket

################################################################################
####CONSTANTS and set up casc paths
CWD = os.getcwd()
face_cascPath = CWD+"/haarcascades/haarcascade_frontalface_alt.xml"
faceCascade = cv2.CascadeClassifier(face_cascPath)
#eye_cascPath = CWD+"/haarcascades/haarcascade_eye.xml"
#eyeCascade = cv2.CascadeClassifier(eye_cascPath)
DETECTED_IMG_DIR = "/detected_faces_imgs"
DETECTED_IMG_Path = CWD+DETECTED_IMG_DIR+"/img"
DETECTED_VD_DIR = "/detected_faces_videos"
DETECTED_VD_Path = CWD+DETECTED_VD_DIR+"/vid"
SERVER_HOST = 'www.google.com'#'localhost'
SERVER_PORT = 80

####  set up save-to dirs
try: 
    os.makedirs(CWD+DETECTED_IMG_DIR)
except OSError:
    if not os.path.isdir(CWD+DETECTED_IMG_DIR):
        raise
try: 
    os.makedirs(CWD+DETECTED_VD_DIR)
except OSError:
    if not os.path.isdir(CWD+DETECTED_VD_DIR):
        raise
        
#### Set up the recognition model
## For face recognition we will the the LBPH Face Recognizer
recognizer = cv2.createLBPHFaceRecognizer(1,8,8,8,100.0)
recognizer.load("./face_recognizer.xml")


#### Training logic here, commented out so not retraining each time program runs
def get_images_and_labels(path):
    ## Append all the absolute image paths in a list image_paths
    image_paths = [os.path.join(path, f) for f in os.listdir(path)]
    images = []
    labels = []
    for image_path in image_paths:
        ## Read the image and convert to grayscale
        image_pil = Image.open(image_path).convert('L')
        ## Convert the image format into numpy array
        image = np.array(image_pil, 'uint8')
        ## Get the label of the image
        nbr = 1 #int(os.path.split(image_path)[1].split(".")[0].replace("subject", ""))
    	images.append(image)
    	labels.append(nbr)
    	cv2.imshow("Adding faces to traning set...", image)
    	cv2.waitKey(50)
    ## return the images list and labels list
    return images, labels
    
## Call the get_images_and_labels function and get the face images and the corresponding labels
#images, labels = get_images_and_labels(CWD+DETECTED_IMG_DIR)
cv2.destroyAllWindows()

## Perform the tranining
#recognizer.train(images, np.array(labels))        
recognizer.save("./face_recognizer.xml")
        
img_cnt = 0
frm_cnt = 0
out = cv2.VideoWriter(DETECTED_VD_Path+".avi", -1, 20.0, (640,480))

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
        minNeighbors=8,
        minSize=(30, 30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE#cv2.CASCADE_SCALE_IMAGE
    )

    messages = [];
    ## Draw a rectangle around the faces
    for (x, y, w, h) in faces:
    	roi = gray[y:y+h,x:x+w] # a face region in current frame
    	nbr_predicted, conf = recognizer.predict(roi)
    	messages.append(str(nbr_predicted)+"#"+str(conf));
    	#print "predicted label: "+str(nbr_predicted)+" conf: "+str(conf)
        #nbr_actual = int(os.path.split(image_path)[1].split(".")[0].replace("subject", ""))
        if 1 == nbr_predicted:
           cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        else:
           cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
        #cv2.imshow("Recognizing Face", roi)
        
        ## write image to the image path
	#cv2.imwrite(DETECTED_IMG_Path+str(img_cnt)+".jpg", roi) 
	
	img_cnt = img_cnt+1
	
    ## Display the resulting frame
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if len(faces)>0: ## save to the video file if faces are detected at this frame
	frm_cnt = frm_cnt+1    ## update frame number
	cur_time = time.time() ## get current UTC time
	out.write(frame)
	for msg in messages:
	    msg = str(frm_cnt)+"#"+str(cur_time)+"#"+msg
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
		

## When everything is done, release the capture
out.release()
video_capture.release()
cv2.destroyAllWindows()
s.close()


