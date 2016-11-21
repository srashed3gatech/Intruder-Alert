############# Intruder-Alert #################
This is a intruder detection system developed for CS6400.

### **Runtime Environment** setup:
1. Install OpenCV 2.4.13 (no versions above 2). Bind python 2.7 to OpenCV.

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


### To update/re-train face classifier: **NOTE: use the updt_Model in source folder**
1. update model:
`python updt_Model.py <user_label> <user_name>` 				
2. re-train model:
`python updt_Model.py <user_label> <user_name> --t` 			
3. look at program description:
`python updt_Model.py -h`




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
