import cv2, sys, os
import numpy as np
from PIL import Image
import argparse
import shutil
from DBUtility import iAlertDB
from classes.RelatedUserInfo import RelatedUserInfo

################################################################################
#### Use this python script to collect or process user pics, use -h for more info on args
################################################################################
#### set up casc paths and save-to dirs
face_cascPath = "../haarcascades/haarcascade_frontalface_alt.xml"
faceCascade = cv2.CascadeClassifier(face_cascPath)
MODEL_PATH = "../face_recognizer.xml"

parser = argparse.ArgumentParser(description="\tProcess or collect images.\n\n")
parser.add_argument("user_label", help="\t\tindicate what number should be used to label the new related user (the one appearing in front of the camera)", type=int)
parser.add_argument("name", help="\t\tindicate the new user's name",type=str)
parser.add_argument("--c", help="\t\tindicate whether you want to collect images from camera and add new users",action="store_true")
args = parser.parse_args()
user_label = args.user_label
user_name = args.name
DETECTED_IMG_DIR = "../detected_faces_imgs/user"+str(user_label)
DETECTED_IMG_Path = DETECTED_IMG_DIR+"/img_"

def collect_img_from_cam():
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
        for i in range (10):
            ret, frame = video_capture.read()
            if ret:
                break
        else:
            # capture failed even after 10 tries
            raise Exception("Video driver does not like me.")
#         ret, frame = video_capture.read()
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
    Interface with DB to save new user after collect the images
    '''
    db = iAlertDB()
    u = RelatedUserInfo(user_label,user_label,DETECTED_IMG_DIR,100)
    u.name = user_name
    db.insert_related_user(u)

def process_images(path):
    img_cnt = 0
    image_paths = [os.path.join(path, f) for f in os.listdir(path)]
    for image_path in image_paths:
#         print image_path
        ## Read the image and convert to grayscale
        image_pil = Image.open(image_path).convert('L')
        image = np.array(image_pil, 'uint8')
        faces = faceCascade.detectMultiScale(image)
        for (x, y, w, h) in faces:
            cv2.imwrite(DETECTED_IMG_DIR+"/img_"+str(img_cnt)+".jpg", image[y: y + h, x: x + w]) 
            img_cnt = img_cnt+1
        os.remove(image_path)
    print("processed images")

if __name__ == "__main__":
    if(args.c):
        collect_img_from_cam()
    else:
        process_images(DETECTED_IMG_DIR)
