###########TODO: FINAL INTEGRATION MEETING 11/20/2016##############
Before the Call:
- Kixin done with alarm-generation / alarm-clear part - and let Mamun know it's ready for integration (by Saturday afternoon 5pm)
- Yaling completed bootloader (create face_recognizer.xml), update_mode (get user picture and enter related_user entry into db) -(By Saturday afternoon 5pm)
- Mamun integated bootloader into iAlertMain and frame, corresponds_to table updated properly (by Sunday Morning 9am)

To Do on Call:
1. Full end to end integration testing - i.e. all codes are functioning correctly
2. Demo Use Case testing
###################################################################


# Intruder-Alert
This is a intruder detection system developed for CS6400.

### **Runtime Environment** setup:
1. Install OpenCV 2.4.13 (no versions above 2). Bind python 2.7 to OpenCV.




### To update/re-train face classifier: **NOTE: use the updt_Model in source folder**
1. update model:
`python updt_Model.py <user_label> <user_name>` 				
2. re-train model:
`python updt_Model.py <user_label> <user_name> --t` 			
3. look at program description:
`python updt_Model.py -h`

### To launch image-capture and face-recognition module:
`python imgCap_RecgMod.py`



### NETWORKING PROTOCOL
Client Socket Write: BUF[i] = \#VID\#FRAME_NUM\#TIME_STAMP\#USER\#CONF


Server Socket

countdown(10s, callback_function)





==========ISSUES TO SOLVE=========
We probably need not to use message bus. We'll use queue class - a builtin one which is synchronized. 
But our program need to be multi-threaded with following functions:

0. There is a global queue object that used for frame exchange between threads
1. Master Thread
	Functions -
	1.1 Create and start camera Cap/Rec/Tra Thread
	1.2 Create and start Db frame writer thread as a timeout manner  (e.g: threading.Timer(2, DBWriter, [params]))
2. Camera Capture, Recognition & Training Thread
	Functions - 
	2.1 Read database user and picture info using function get_related_user_info() 
	2.2 Train and generate face_recognizer.xml
	2.3 Create a new video file and enter info into db
	2.4 Enter into loop where it detect and recognize image and enqueue necessary frame (VideoFrame object) to threaded queue
3. Database Frame writer Thread
	Functions
	3.1 dequeue MAX_WRITE_FRAME = 10 from global queue
	3.2 Using sqlalchemy write frame into tables: frame, corresponds to (as applicable)

TODO:
~ Threaded queue creation
~ Skeleton of Multithreaded program
~ Database Writer thread creation
~ Integrate current codes into skeleton
~ 

Research Item:
~ How to create alarm from frames

	
===== Prepare dev machine ======

::Setting UP the MAC ENV::

1. Install Brew
2. brew install opencv
3. brew install Homebrew/python/pillow
4. Install Eclipse
5. download plugin pydev for eclipse
6. download git plugin for eclipse
7. Pull git project 

Python MYSQL Connection & Other modules:
brew install mysql-connector-c
pip install mysql-python

Install database abstraction library: pip install SQLAlchemy
Install database driver: pip install --proxy one.proxy.att.com:8080 pymysql 
Install intra-thread message passing: pip install PyDispatcher

Setting up database:
install xampp 5.5.28
install mysql-workbench


===================Message BUS Research=================
Ref: http://pydispatcher.sourceforge.net/

generic: 
pip install PyDispatcher
behind proxy: pip install --proxy user:password@proxyserver:port PyDispatcher

Example:http://bazaar.launchpad.net/~mcfletch/pydispatcher/working/files

I've reserached other message Bus systems which is overly complicated (doesn't worth spending time)
here is one of the reference: https://python-can.readthedocs.io/en/latest/interfaces/socketcan.html

============Alarm Generation from Frame Research========
=== alarm creation/tallying process ====
1. Do I see any Stranger Frame? 
	Y -> check if any INTRUDER ALARM (cate_name) exist and Clear_Time = null
		Y -> tally++ , update last_occ = current timestamp
        N -> INSERT INTO ALARM (... first_occ=timestamp, last_occ=timestamp 'INTRUDER ALARM', tally = 0, clear_time = null)
2. Do I see any Stranger Frame? Y - follow ste-1
	N - do nothing

== alarm clearing process ===
alarm clearing threshold = 10min
every 10 min:
	UPDATE ALARM set clear_time = now where time_now - last_occ > 10min
