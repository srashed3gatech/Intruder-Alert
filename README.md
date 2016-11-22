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
	
==============Stored Procedure==========
DELIMITER //
CREATE PROCEDURE generate_alarm
(IN alarm_category VARCHAR(45), IN tally_threshold INT(11))

BEGIN

/*1. Check if we need to insert alarm*/

DECLARE LAST_RUN_TIME TIMESTAMP;
SELECT STR_TO_DATE(SYSTEM_INFO.value,'%Y-%m-%d %k:%i:%s') INTO LAST_RUN_TIME
	FROM SYSTEM_INFO 
	WHERE SYSTEM_INFO.key = 'ALARM_GENERATOR_LASTRUN' LIMIT 1;

IF (LAST_RUN_TIME is NULL) THEN
	SIGNAL SQLSTATE '77777'
      SET MESSAGE_TEXT = 'SET ALARM_GENERATOR_LASTRUN in SYSTEM_INFO TABLE';
END IF; 

DECLARE ALARMED_FRAME_COUNT INT(11);
DECLARE ALARMED_FRAME_TIMESTAMP TIMESTAMP;
DECLARE ALARMED_FRAME_MAX_TIMESTAMP TIMESTAMP; 
SELECT count(f.frame_num) into ALARMED_FRAME_COUNT, 
	min(f.timestamp) into ALARMED_FRAME_TIMESTAMP,
	max(f.timestamp) into ALARMED_FRAME_MAX_TIMESTAMP
	FROM frame f
	where f.timestamp > LAST_RUN_TIME
	AND (f.video_id, f.frame_num) NOT IN (
		SELECT ff.video_id, ff.frame_num
		FROM frame ff
		JOIN 
		CORRESPONDS_TO c ON (ff.video_id=c.video_id AND ff.frame_num = c.frame_num)
		where ff.timestamp > LAST_RUN_TIME
	) LIMIT 1;

IF (ALARMED_FRAME_COUNT > 0 AND ALARMED_FRAME_TIMESTAMP is not NULL) THEN
	/*get if same alarm exist and not cleared*/
	DECLARE ALARM_ID INT(11);
	DECLARE TALLY_COUNT INT(11);

	SELECT alarm_id into ALARM_ID, tally into TALLY_COUNT 
		FROM ALARM 
		WHERE cate_name = alarm_category AND clear_time IS NOT NULL;
	

	START TRANSACTION;
	
	IF (ALARM_ID IS NOT NULL AND TALLY_COUNT+1 > tally_threshold) OR (ALARM_ID IS NULL) THEN
		/*insert alarm table entry*/
		INSERT INTO ALARM(first_occ, last_occ, tally, cate_name) 
			VALUES(ALARMED_FRAME_TIMESTAMP, ALARMED_FRAME_TIMESTAMP, 0, alarm_category);
		
		SET last_alarm_id = LAST_INSERT_ID();
		
		/*Inset alarm generated from frames*/
		INSERT INTO GENERATED_FROM(video_id, frame_num, alarm_id)
			SELECT f.video_id, f.frame_num, last_alarm_id
			FROM frame f
			where f.timestamp > dateLastRun
			AND (f.video_id, f.frame_num) NOT IN (
				SELECT ff.video_id, ff.frame_num
				FROM frame ff
				JOIN 
				CORRESPONDS_TO c ON (ff.video_id=c.video_id AND ff.frame_num = c.frame_num)
				where ff.timestamp > dateLastRun
			);
	ELSE
		UPDATE ALARM SET tally = tally + 1 WHERE alarm_id = ALARM_ID;
	END IF;
	
	UPDATE SYSTEM_INFO SET value = ALARMED_FRAME_MAX_TIMESTAMP WHERE key = 'ALARM_GENERATOR_LASTRUN';
	COMMIT;
	
END IF;



END //
DELIMITER ;



END //
DELIMITER ;