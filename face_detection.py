import cv2
import sys
import os

################################################################################
# set up casc paths and save-to dirs
CWD = os.getcwd()
face_cascPath = CWD+"/haarcascades/haarcascade_frontalface_alt.xml"
#eye_cascPath = CWD+"/haarcascades/haarcascade_eye.xml"
faceCascade = cv2.CascadeClassifier(face_cascPath)
#eyeCascade = cv2.CascadeClassifier(eye_cascPath)

DETECTED_IMG_DIR = "/detected_faces_imgs"
DETECTED_IMG_Path = CWD+DETECTED_IMG_DIR+"/img"
try: 
    os.makedirs(CWD+DETECTED_IMG_DIR)
except OSError:
    if not os.path.isdir(CWD+DETECTED_IMG_DIR):
        raise
img_cnt = 0
DETECTED_VD_DIR = "/detected_faces_videos"
DETECTED_VD_Path = CWD+DETECTED_VD_DIR+"/vid"
try: 
    os.makedirs(CWD+DETECTED_VD_DIR)
except OSError:
    if not os.path.isdir(CWD+DETECTED_VD_DIR):
        raise
#vid_cnt = 0
#new_vid = True
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(DETECTED_VD_Path+".avi", fourcc, 20.0, (640,480))

video_capture = cv2.VideoCapture(0)
while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.15,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    #print DETECTED_FC_Path+str(img_cnt)+".jpg"
    #cv2.imwrite(DETECTED_FC_Path+str(img_cnt)+".jpg", frame)
    #break

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
	roi = gray[y:y+h,x:x+w]
	cv2.imwrite(DETECTED_IMG_Path+str(img_cnt)+".jpg", roi) 
	img_cnt = img_cnt+1
	

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if len(faces)==0: #if no face detected
	#new_vid = True
	#out.release()
	continue
    else: #save to the video file if faces are detected at this frame
	#if new_vid:
	#	out = cv2.VideoWriter(DETECTED_VD_Path+'/output.avi', fourcc, 20.0, (640,480))
	#	new_vid = False
	#	vid_cnt = vid_cnt+1
	out.write(frame)
		

# When everything is done, release the capture
out.release()
video_capture.release()
cv2.destroyAllWindows()
