# Intruder-Alert
This is a intruder detection system developed for CS6400.

### **Runtime Environment** setup:
1. Install OpenCV 2.4.13 (no versions above 2). Bind python 2.7 to OpenCV.




### To update/re-train face classifier:
1. update model:
`python updt_Model.py <user_label>` 				
2. re-train model:
`python updt_Model.py <user_label> --t` 			
3. look at program description:
`python updt_Model.py -h`

### To launch image-capture and face-recognition module:
`python imgCap_RecgMod.py`



### NETWORKING PROTOCOL
Client Socket Write: BUF[i] = \#VID\#FRAME_NUM\#TIME_STAMP\#USER\#CONF


Server Socket

countdown(10s, callback_function)




BUFF_QUEUE


synchronized
funciton callback_function(){
    //flush the buffer; 
    
    
    //create db connction
    server = ;';
    port = '''
    driver =/'/
    
    db = mysql_connect()
    
    foreach(item in BUFF_QUEUE){
        itemArr = split(ite,. '$#'
       db.insert("INSERT INTO FRAME VALUES
        (itemARR[0], itemARR[1], itemARR[2], itemARR[3])"),
        ()       
    }
 

}

==========ISSUES TO SOLVE=========
1. imgCap_RecgMod.py
	- recognizing person isn't constant it continuously jump between recog or not recog and return spurious frames
2. tcpServer_IA.py
	- discontinue
3. Camera Capture, Recognition & Training Module
	3.1 Read user-id from related user and train the model with related user picture
	3.2 Write video file id and path to video table which is saving current video
	3.3 Make sure write new video file id in case we need to roll over to a new video file
	3.4 Write frame on the message bus
4. Message Bus
	4.1 research item [mamun]
5. DBController
	5.1 Communicates with Message bus / grab available data and write frame into Database
	5.2 Provide bunch of functions to use
		5.2.1 write_from_message_bus()
		5.2.2 write_new_video_file() - used by 3.2 / 3.3
		5.2.3 read_related_user_info() - used by 3.1
6. DBMiner
	6.1 Research item
	
===== Prepare dev machine ======
::Setting UP the MAC ENV::

1. Install Brew
2. brew install opencv
3. brew install Homebrew/python/pillow
4. Install Eclipse
5. download plugin pydev for eclipse
6. download git plugin for eclipse
7. Pull git project 

Python MYSQL COnnection:
brew install mysql-connector-c
pip install mysql-python

pip install SQLAlchemy

Setting up database:
install xampp 5.5.28
install mysql-workbench

