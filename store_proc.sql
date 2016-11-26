---
--- Alarm Gnerator - to be called from DB_Frame_Writer.run()
---

DELIMITER //
DROP PROCEDURE IF EXISTS generate_alarm
//
CREATE PROCEDURE generate_alarm(
	IN alarm_category VARCHAR(45), 
	IN tally_threshold INT(11)
)

BEGIN
DECLARE LAST_RUN_TIME TIMESTAMP;
DECLARE ALARMED_FRAME_COUNT INT(11);
DECLARE ALARMED_FRAME_MIN_TIMESTAMP TIMESTAMP;
DECLARE ALARMED_FRAME_MAX_TIMESTAMP TIMESTAMP; 
DECLARE ALARM_ID INT(11);
DECLARE TALLY_COUNT INT(11);
DECLARE last_alarm_id INT(11);
DECLARE exit handler for SQLEXCEPTION
        BEGIN
        ROLLBACK;
		RESIGNAL;
    END;
/*TRUNCATE sp_log;
INSERT INTO sp_log(log_msg) values(concat("Debug: Begin attributes alarm_category: ", alarm_category, " tally_threshold: ", tally_threshold, "\n"));*/
/*Timestamp after which we need to read frame*/
(SELECT str_to_date(s.value,'%Y-%m-%d %k:%i:%s') INTO LAST_RUN_TIME
						FROM SYSTEM_INFO s
						WHERE s.key = 'ALARM_GENERATOR_LASTRUN' LIMIT 1);

IF(LAST_RUN_TIME is NULL) THEN
	SIGNAL SQLSTATE '77777' 
		SET MESSAGE_TEXT = 'SET ALARM_GENERATOR_LASTRUN in SYSTEM_INFO TABLE';
END IF;

/*1. Check if we need to insert alarm*/
SELECT count(f.frame_num), min(f.timestamp), max(f.timestamp) 
		INTO ALARMED_FRAME_COUNT, ALARMED_FRAME_MIN_TIMESTAMP, ALARMED_FRAME_MAX_TIMESTAMP
	FROM frame f
	where f.timestamp > LAST_RUN_TIME
	AND (f.video_id, f.frame_num) NOT IN (
		SELECT ff.video_id, ff.frame_num
		FROM frame ff
		JOIN 
		CORRESPONDS_TO c ON (ff.video_id=c.video_id AND ff.frame_num = c.frame_num)
		where ff.timestamp > LAST_RUN_TIME
	) LIMIT 1;

/*INSERT INTO sp_log(log_msg) values(concat("Debug: Starting Transaction Before IF"));*/
START TRANSACTION;
IF (ALARMED_FRAME_COUNT > 0 AND ALARMED_FRAME_MIN_TIMESTAMP is not NULL) THEN
	/*get if same alarm exist and not cleared*/
	/*INSERT INTO sp_log(log_msg) values(concat("Debug: in IF => ALARMED_FRAME_MIN_TIMESTAMP: ", ALARMED_FRAME_MIN_TIMESTAMP, " ALARMED_FRAME_COUNT: ", ALARMED_FRAME_COUNT, "\n"));*/

	SELECT a.alarm_id, a.tally INTO ALARM_ID, TALLY_COUNT
		FROM ALARM a
		WHERE a.cate_name = alarm_category 
		AND a.clear_time IS NULL 
		order by a.alarm_id desc
		LIMIT 1;

	/*SELECT ALARM_ID, TALLY_COUNT;*/

	/*INSERT INTO sp_log(log_msg) values(concat("ALARM_ID: ",ALARM_ID, "TALLY_COUNT: ", TALLY_COUNT));*/
	
	IF (ALARM_ID IS NULL) OR ( (ALARM_ID >= 0) AND (TALLY_COUNT >= tally_threshold) ) THEN
		/*INSERT INTO sp_log(log_msg) values(concat("Debug: in IF => ALARM_ID: ", ALARM_ID, " TALLY_COUNT: ", TALLY_COUNT, "\n"));*/
		/*insert alarm table entry*/
		INSERT INTO ALARM(first_occ, last_occ, tally, cate_name) 
			VALUES(ALARMED_FRAME_MIN_TIMESTAMP, ALARMED_FRAME_MAX_TIMESTAMP, 0, alarm_category);
		
		SET last_alarm_id := LAST_INSERT_ID();
		
		/*Inset alarm generated from frames*/
		INSERT INTO GENERATED_FROM(video_id, frame_num, alarm_id)
			SELECT f.video_id, f.frame_num, last_alarm_id
			FROM frame f
			where f.timestamp > LAST_RUN_TIME
			AND (f.video_id, f.frame_num) NOT IN (
				SELECT ff.video_id, ff.frame_num
				FROM frame ff
				JOIN 
				CORRESPONDS_TO c ON (ff.video_id=c.video_id AND ff.frame_num = c.frame_num)
				where ff.timestamp > LAST_RUN_TIME
			);
	ELSE
		/*INSERT INTO sp_log(log_msg) values(concat("Debug: in ELSE => ALARM_ID: ", ALARM_ID, " TALLY_COUNT: ", TALLY_COUNT, "\n"));*/
		UPDATE ALARM SET tally = TALLY_COUNT + 1 WHERE alarm_id = ALARM_ID;
		
		/*Inset alarm generated from frames*/
		INSERT INTO GENERATED_FROM(video_id, frame_num, alarm_id)
			SELECT f.video_id, f.frame_num, ALARM_ID
			FROM frame f
			where f.timestamp > LAST_RUN_TIME
			AND (f.video_id, f.frame_num) NOT IN (
				SELECT ff.video_id, ff.frame_num
				FROM frame ff
				JOIN 
				CORRESPONDS_TO c ON (ff.video_id=c.video_id AND ff.frame_num = c.frame_num)
				where ff.timestamp > LAST_RUN_TIME
			);
	END IF;
	/*INSERT INTO sp_log(log_msg) values(concat("Debug: Transaction END, updating ALARMED_FRAME_MAX_TIMESTAMP: ", ALARMED_FRAME_MAX_TIMESTAMP));*/
	UPDATE SYSTEM_INFO s SET s.value = ALARMED_FRAME_MAX_TIMESTAMP WHERE s.key = 'ALARM_GENERATOR_LASTRUN';
COMMIT;
	
END IF;
END
//DELIMITER ;
