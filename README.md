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

File: alarm_generator.py

1. Get ALARM_GENERATOR_LASTRUN from SYSTEM_INFO
2. SELECT count(f.frame_num), min(f.timestamp) 
	FROM frame f
	where f.timestamp > curdate()
	AND (f.video_id, f.frame_num) NOT IN (
		SELECT ff.video_id, ff.frame_num
		FROM frame ff
		JOIN 
		CORRESPONDS_TO c ON (ff.video_id=c.video_id AND ff.frame_num = c.frame_num)
		where ff.timestamp > curdate()
	)
3. Generate an intruder cetegory alarm [IA]
4. IF IA exists & not clear then
		IF ++tally > 360 (considering alarm generator run every 10 s)
			clear old IA
			INSERT new IA with tally = 0
		ELSE
			update tally++
	ELSE
		INSERT new IA with tally = 0

DBUtility.py
	GetAlarmedFrameCount():
		
	GetAlarmedFrames(): count of alarm & min timestamp
		SELECT f.*
			FROM frame f
			where f.timestamp > curdate()-1
			AND (f.video_id, f.frame_num) NOT IN (
				SELECT ff.video_id, ff.frame_num
				FROM frame ff
				JOIN 
				CORRESPONDS_TO c ON (ff.video_id=c.video_id AND ff.frame_num = c.frame_num)
				where ff.timestamp > curdate()-1
			)
	
	GetAlarmNotCleared(ALARM_CATEGORY):
		//alarm id exists in the db
	
	GetAlarmById(id)
	
	ClearAlarm(alarmId)
	
	InsertAlarms(AlarmObj)
	
	UpdateAlarm(AlarmObj) 
		 
		ALARMS / GENERATED-FROM
	Read_System_Info(key = "ALARM_GENERATOR_LASTRUN")
	
