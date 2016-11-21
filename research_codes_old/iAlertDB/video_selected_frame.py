import numpy as np
import cv2

#Get video name from user
#Ginen video name must be in quotes, e.g. "pirkagia.avi" or "plaque.avi"
#video_name = input("Please give the video name including its extension. E.g. \"pirkagia.avi\":\n")
video_name = "../Video/cam_cap_20161120-075350.avi"

#Open the video file
cap = cv2.VideoCapture(video_name)
fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
print "FPS: "+ str(fps)

capSize = (str(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),
        str(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))#(640,480) # this is the size of my source video
print "WIDTH/HEIGHT: " + capSize

#Set frame_no in range 0.0-1.0
#In this example we have a video of 30 seconds having 25 frames per seconds, thus we have 750 frames.
#The examined frame must get a value from 0 to 749.
#For more info about the video flags see here: http://stackoverflow.com/questions/11420748/setting-camera-parameters-in-opencv-python
#Here we select the last frame as frame sequence=749. In case you want to select other frame change value 749.
#BE CAREFUL! Each video has different time length and frame rate. 
#So make sure that you have the right parameters for the right video!
'''
fps=30
frame_seq = 71
time_length = (frame_seq + 1) * fps
frame_no = (frame_seq /(time_length*fps))

#The first argument of cap.set(), number 2 defines that parameter for setting the frame selection.
#Number 2 defines flag CV_CAP_PROP_POS_FRAMES which is a 0-based index of the frame to be decoded/captured next.
#The second argument defines the frame number in range 0.0-1.0
cap.set(2,frame_no);

#Read the next frame from the video. If you set frame 749 above then the code will return the last frame.
ret, frame = cap.read()

#Set grayscale colorspace for the frame. 
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#Cut the video extension to have the name of the video
my_video_name = video_name.split(".")[0]

#Display the resulting frame
cv2.imshow(my_video_name+' frame '+ str(frame_seq),gray)

#Set waitKey 
cv2.waitKey()

#Store this frame to an image
cv2.imwrite(my_video_name+'_frame_'+str(frame_seq)+'.jpg',gray)'''

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()