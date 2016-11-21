import cv2 
import time

filename = time.strftime("%m-%d-%H-%M-%S") + '.avi' 
cap = cv2.VideoCapture(0) 
cap.set(3 , 640) #'''cv2.cv.CV_CAP_PROP_FRAME_WIDTH''' 
cap.set(4 , 480) #'''cv2.cv.CV_CAP_PROP_FRAME_WIDTH'''
#time.sleep(10)
size = (int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),
        int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))

print size

fps = 16

fourcc  = cv2.cv.FOURCC('X', 'V', 'I', 'D')     #does not work 
fourcc0 = cv2.cv.FOURCC('D', 'I', 'V', 'X')     #does not work 
fourcc1 = cv2.cv.FOURCC('M', 'J', 'P', 'G')     #does not work 
fourcc2 = cv2.cv.FOURCC('8', 'B', 'P', 'S')     #works, large 
fourcc3 = cv2.cv.FOURCC('A', 'V', 'R', 'N')     #does not work 
fourcc4 = cv2.cv.FOURCC('R', 'P', 'Z', 'A')     #does not work 
fourcc5 = cv2.cv.FOURCC('S', 'V', '1', '0')     #does not work 
fourcc6 = cv2.cv.FOURCC('S', 'V', 'Q', '3')     #works, small 
fourcc7 = cv2.cv.FOURCC('Z', 'Y', 'G', 'O')     #does not work

out = cv2.VideoWriter(filename, fourcc6, fps, (640,480), True)
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        out.write(frame)
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break;

    else:
        print 'Error...'
        break;

cap.release() 