import cv2, sys, os
import numpy as np
from PIL import Image
import argparse
import shutil
from DBUtility import iAlertDB
from classes.RelatedUserInfo import RelatedUserInfo

################################################################################
#### Use this python script to update/train the model, use -h for more info on args
################################################################################
#### set up casc paths and save-to dirs
CWD = os.getcwd()
face_cascPath = "../haarcascades/haarcascade_frontalface_alt.xml"
#eye_cascPath = CWD+"/haarcascades/haarcascade_eye.xml"
faceCascade = cv2.CascadeClassifier(face_cascPath)
#eyeCascade = cv2.CascadeClassifier(eye_cascPath)
MODEL_PATH = "../face_recognizer.xml"

parser = argparse.ArgumentParser(description="\tNew user image capture and update model: First step is to capture your images via webcam, hit 'q' when you think you are done collecting images. Then the program will automatically train/update the model.\n\n")
parser.add_argument("user_label", help="\t\tindicate what number should be used to label the new related user (the one appearing in front of the camera)", type=int)
parser.add_argument("name", help="\t\tindicate the new user's name",type=str)
parser.add_argument("--t", help="\t\tindicate whether you want to retrain to a completely new model, if not specified, will update the model",action="store_true")
args = parser.parse_args()
user_label = args.user_label
user_name = args.name
DETECTED_IMG_DIR = CWD+"/../detected_faces_imgs/user"+str(user_label)
DETECTED_IMG_Path = DETECTED_IMG_DIR+"/img_"

## remove all previous images in that user's dir
if(os.path.isdir(DETECTED_IMG_DIR)):
    shutil.rmtree(DETECTED_IMG_DIR)
try: 
    os.makedirs(DETECTED_IMG_DIR)
except OSError:
    if not os.path.isdir(DETECTED_IMG_DIR):
        raise
        
img_cnt = 0
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

    ## Draw a rectangle around the faces
    for (x, y, w, h) in faces:
    	roi = gray[y:y+h,x:x+w] # a face region in current frame
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.imshow("Recognizing Face", roi)
        ## write image to the image path
	cv2.imwrite(DETECTED_IMG_Path+str(user_label)+"_"+str(img_cnt)+".jpg", roi) 
	img_cnt = img_cnt+1
	
    ## Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
		
## When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()

'''
Interface with DB to save new user
TODO: get User name and conf_thresh? now 100 is the default conf thresh
'''
db = iAlertDB()
u = RelatedUserInfo(user_label,user_label,DETECTED_IMG_DIR,100)
u.name = user_name
db.insert_related_user(u)

#### training the recognition model after new user image captures
## For face recognition we will the the LBPH Face Recognizer
recognizer = cv2.createLBPHFaceRecognizer(1,8,8,8,123.0)
if os.path.exists(MODEL_PATH): 
    recognizer.load(MODEL_PATH)
#### Training logic here, commented out so not retraining each time program runs
def get_images_and_labels(path):
    ## Append all the absolute image paths in a list image_paths
    image_paths = [os.path.join(path, f) for f in os.listdir(path)]
    ## face images
    images = []
    ## labels
    labels = []
    for image_path in image_paths:
        ## Read the image and convert to grayscale
        image_pil = Image.open(image_path).convert('L')
        ## Convert the image format into numpy array
        image = np.array(image_pil, 'uint8')
        ## Get the label of the image
        nbr = int(os.path.split(path)[1].split(".")[0].replace("user", ""))
    	images.append(image)
    	labels.append(nbr)
    	cv2.imshow("Adding faces to traning set...", image)
    	cv2.waitKey(50)
    ## return the images list and labels list
    return images, labels
## Call the get_images_and_labels function and get the face images and the corresponding labels
images, labels = get_images_and_labels(DETECTED_IMG_DIR)
cv2.destroyAllWindows()
## Perform the tranining or updating
if(args.t):
    recognizer.train(images, np.array(labels))
else:
    recognizer.update(images, np.array(labels))        
recognizer.save(MODEL_PATH)


