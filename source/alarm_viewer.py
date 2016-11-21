import numpy as np
import cv2
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
'''show video by given id and read corresponding frames associated to the alarm and show only the alarmed frames'''

#TODO: Write video to a file with only frames that contain alarms (used by emailer)
# return new video file

def writeTempVideo(video_src_file, alarm_frames):
    cap = cv2.VideoCapture(video_src_file)
    cap.set(3 , 320) #width 320
    cap.set(4 , 240) #height 240
    while(cap.isOpened()):
        ret, frame = cap.read()
        
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    
def emailIAlert(video_src_file, emailAddress):
    fromaddr = "srashed3gatech@gmail.com"
    toaddr = emailAddress
    
    msg = MIMEMultipart()
    
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "!!Intruder!!"
    
    body = "iAlert detected intruder on monitored premise... please check attached video for detail"
    
    msg.attach(MIMEText(body, 'plain'))
    
    filename = "alarmvideo.avi"
    attachment = open(video_src_file, 'rb')
    
    part = MIMEBase('application', 'octate-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename= %s' %filename)
    
    msg.attach(part)
    
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(fromaddr, '2003260028')
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    
if __name__ == "__main__":
    #writeTempVideo("sample.avi", alarm_frames)
    emailIAlert("sample.avi","")