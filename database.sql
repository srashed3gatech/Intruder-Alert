CREATE SCHEMA ialertdb ;

USE ialertdb;

--
-- Table structure for table USER
--

DROP TABLE IF EXISTS USER;
CREATE TABLE USER (
  user_id varchar(15) NOT NULL,
  name varchar(45) NOT NULL,
  PRIMARY KEY (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table SYSTEM_USER
--

DROP TABLE IF EXISTS SYSTEM_USER;
CREATE TABLE SYSTEM_USER (
  user_id varchar(15) NOT NULL,
  email varchar(45) NOT NULL,
  password varchar(45) NOT NULL DEFAULT 'password',
  PRIMARY KEY (user_id),
  CONSTRAINT fk_system_user_id FOREIGN KEY (user_id) REFERENCES USER (user_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


--
-- Table structure for table VIDEO
--

DROP TABLE IF EXISTS VIDEO;
CREATE TABLE VIDEO (
  video_id int(11) NOT NULL AUTO_INCREMENT,
  time_created datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  duration_sec double NOT NULL,
  video_path varchar(255) NOT NULL,
  framerate int(11) NOT NULL DEFAULT '30',
  expiry datetime NOT NULL,
  PRIMARY KEY (video_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table SYSTEM_INFO
--

DROP TABLE IF EXISTS SYSTEM_INFO;
CREATE TABLE SYSTEM_INFO (
  `key` varchar(255) NOT NULL,
  `value` varchar(255) NOT NULL,
  PRIMARY KEY (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table RELATED_USER
--

DROP TABLE IF EXISTS RELATED_USER;
CREATE TABLE RELATED_USER (
  user_id varchar(15) NOT NULL,
  conf_level_thresh decimal(3,0) NOT NULL,
  PRIMARY KEY (user_id),
  CONSTRAINT fk_related_user_id FOREIGN KEY (user_id) REFERENCES USER (user_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table RELATED_USER_PICTURE
--

DROP TABLE IF EXISTS RELATED_USER_PICTURE;
CREATE TABLE RELATED_USER_PICTURE (
  user_id varchar(15) NOT NULL,
  pic_id int(11) NOT NULL,
  pic_path varchar(256) NOT NULL,
  PRIMARY KEY (user_id,pic_id),
  CONSTRAINT fk_related_user_id_picture FOREIGN KEY (user_id) REFERENCES USER (user_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table FRAME
--

DROP TABLE IF EXISTS FRAME;
CREATE TABLE FRAME (
  video_id int(11) NOT NULL,
  frame_num bigint(100) NOT NULL,
  timestamp datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (video_id,frame_num),
  CONSTRAINT fk_frame_videoid FOREIGN KEY (video_id) REFERENCES VIDEO (video_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table CORRESPONDS_TO
--

DROP TABLE IF EXISTS CORRESPONDS_TO;
CREATE TABLE CORRESPONDS_TO (
  user_id varchar(15) NOT NULL,
  video_id int(11) NOT NULL,
  frame_num bigint(100) unsigned NOT NULL,
  conf_level double NOT NULL,
  face_num int(11) DEFAULT NULL,
  PRIMARY KEY (user_id,video_id,frame_num),
  KEY fk_corr_videoid_idx (video_id),
  KEY fk_corr_framenum_idx (frame_num),
  CONSTRAINT fk_corr_userid FOREIGN KEY (user_id) REFERENCES USER (user_id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_corr_videoid_frameid FOREIGN KEY (video_id) REFERENCES FRAME (video_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table ALARM_CATEGORY
--

DROP TABLE IF EXISTS ALARM_CATEGORY;
CREATE TABLE ALARM_CATEGORY (
  cate_name varchar(45) NOT NULL,
  description varchar(255) DEFAULT NULL,
  PRIMARY KEY (cate_name)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table CONFIGS
--

DROP TABLE IF EXISTS CONFIGS;
CREATE TABLE CONFIGS (
  user_id varchar(15) NOT NULL,
  cate_name varchar(45) NOT NULL,
  deferral_time_sec int(11) NOT NULL DEFAULT '60',
  PRIMARY KEY (user_id,cate_name),
  KEY fk_config_alarm_category_idx (cate_name),
  CONSTRAINT fk_config_alarm_category FOREIGN KEY (cate_name) REFERENCES ALARM_CATEGORY (cate_name) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_config_user_id FOREIGN KEY (user_id) REFERENCES USER (user_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table ALARM
--

DROP TABLE IF EXISTS ALARM;
CREATE TABLE ALARM (
  alarm_id int(11) NOT NULL AUTO_INCREMENT,
  first_occ datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tally int(11) NOT NULL DEFAULT '0',
  clear_time datetime DEFAULT NULL,
  cate_name varchar(45) DEFAULT NULL,
  PRIMARY KEY (alarm_id),
  KEY fk_category_name_idx (cate_name),
  CONSTRAINT fk_category_name FOREIGN KEY (cate_name) REFERENCES ALARM_CATEGORY (cate_name) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table GENERATED_FROM
--

DROP TABLE IF EXISTS GENERATED_FROM;
CREATE TABLE GENERATED_FROM (
  video_id int(11) NOT NULL,
  frame_num bigint(100) NOT NULL,
  alarm_id int(11) NOT NULL,
  PRIMARY KEY (video_id,frame_num),
  KEY fk_genfrom_frameno_idx (frame_num),
  KEY fk_genfrom_alarmid_idx (alarm_id),
  CONSTRAINT fk_genfrom_alarmid FOREIGN KEY (alarm_id) REFERENCES ALARM (alarm_id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_genfrom_frameno FOREIGN KEY (video_id, frame_num) REFERENCES FRAME (video_id, frame_num) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


--
-- Table structure for table SENT_TO
--

DROP TABLE IF EXISTS SENT_TO;
CREATE TABLE SENT_TO (
  user_id varchar(15) NOT NULL,
  alarm_id int(11) NOT NULL,
  status int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (user_id,alarm_id),
  KEY fk_sentto_alarmid_idx (alarm_id),
  CONSTRAINT fk_sentto_alarmid FOREIGN KEY (alarm_id) REFERENCES ALARM (alarm_id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_sentto_userid FOREIGN KEY (user_id) REFERENCES USER (user_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Creating View as it looks like corresponding classes
--

CREATE  OR REPLACE VIEW recog_users AS
	SELECT * 
	FROM RELATED_USER
	JOIN RELATED_USER_PICTURE
	USING (user_id);

--
-- Alarm last occurrane column needed
--

ALTER TABLE ialertdb.ALARM 
ADD COLUMN last_occ DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP AFTER first_occ;


--
-- Delete all data - flush
--
-- DELETE FROM CORRESPONDS_TO;
-- DELETE FROM GENERATED_FROM;
-- DELETE FROM SENT_TO;
-- DELETE FROM FRAME;
-- DELETE FROM VIDEO;
-- DELETE FROM ALARM;


-- DELETE FROM RELATED_USER_PICTURE;
-- DELETE FROM RELATED_USER;
-- DELETE FROM SYSTEM_USER;
-- DELETE FROM USER;
-- DELETE FROM SYSTEM_INFO;
	

--
-- Alarm Gnerator - to be called from DB_Frame_Writer.run()
--
INSERT INTO SYSTEM_INFO VALUES('ALARM_GENERATOR_LASTRUN', current_timestamp());

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
	FROM FRAME f
	where f.timestamp > LAST_RUN_TIME
	AND (f.video_id, f.frame_num) NOT IN (
		SELECT ff.video_id, ff.frame_num
		FROM FRAME ff
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
			FROM FRAME f
			where f.timestamp > LAST_RUN_TIME
			AND (f.video_id, f.frame_num) NOT IN (
				SELECT ff.video_id, ff.frame_num
				FROM FRAME ff
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
			FROM FRAME f
			where f.timestamp > LAST_RUN_TIME
			AND (f.video_id, f.frame_num) NOT IN (
				SELECT ff.video_id, ff.frame_num
				FROM FRAME ff
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

--
-- Unprocessed open alarm view
--
CREATE VIEW unprocessed_open_alarm AS
    select 
        a.alarm_id AS alarm_id,
        a.cate_name AS cate_name,
        a.first_occ AS first_occ,
        a.last_occ AS last_occ,
        a.tally AS tally,
        a.clear_time AS clear_time,
        g.video_id AS video_id,
        v.video_path AS video_path,
        g.frame_num AS frame_num
    from
        ((ALARM a)
        join (GENERATED_FROM g
        join VIDEO v ON ((v.video_id = g.video_id))))
    where
        ((a.alarm_id = g.alarm_id)
            and isnull(a.clear_time)
			and a.alarm_id NOT IN (SELECT s.alarm_id FROM SENT_TO s))
    order by a.alarm_id , g.frame_num;
    
--
-- populate one system user, 10 related users
--

SET FOREIGN_KEY_CHECKS = 0; 
TRUNCATE ialertdb.USER;
TRUNCATE ialertdb.RELATED_USER;
TRUNCATE ialertdb.RELATED_USER_PICTURE;
TRUNCATE ialertdb.SYSTEM_USER;
SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO `ialertdb`.`USER` (`user_id`, `name`) VALUES ('1', 'Yaling');
INSERT INTO `ialertdb`.`USER` (`user_id`, `name`) VALUES ('2', 'Mam');
INSERT INTO `ialertdb`.`USER` (`user_id`, `name`) VALUES ('3', 'Kexin');
INSERT INTO `ialertdb`.`USER` (`user_id`, `name`) VALUES ('4', 'Bob');
INSERT INTO `ialertdb`.`USER` (`user_id`, `name`) VALUES ('5', 'Steve');
INSERT INTO `ialertdb`.`USER` (`user_id`, `name`) VALUES ('6', 'Cindy');
INSERT INTO `ialertdb`.`USER` (`user_id`, `name`) VALUES ('7', 'Sarah');
INSERT INTO `ialertdb`.`USER` (`user_id`, `name`) VALUES ('8', 'Gina');
INSERT INTO `ialertdb`.`USER` (`user_id`, `name`) VALUES ('9', 'Alier');
INSERT INTO `ialertdb`.`USER` (`user_id`, `name`) VALUES ('10', 'Tom');

INSERT INTO `ialertdb`.`SYSTEM_USER` (`user_id`, `email`, `password`) VALUES ('1', 'ialert6400@gmail.com', '1234567890;');

INSERT INTO `ialertdb`.`RELATED_USER` (`user_id`, `conf_level_thresh`) VALUES ('1', '100');
INSERT INTO `ialertdb`.`RELATED_USER` (`user_id`, `conf_level_thresh`) VALUES ('2', '100');
INSERT INTO `ialertdb`.`RELATED_USER` (`user_id`, `conf_level_thresh`) VALUES ('3', '100');
INSERT INTO `ialertdb`.`RELATED_USER` (`user_id`, `conf_level_thresh`) VALUES ('4', '100');
INSERT INTO `ialertdb`.`RELATED_USER` (`user_id`, `conf_level_thresh`) VALUES ('5', '100');
INSERT INTO `ialertdb`.`RELATED_USER` (`user_id`, `conf_level_thresh`) VALUES ('6', '100');
INSERT INTO `ialertdb`.`RELATED_USER` (`user_id`, `conf_level_thresh`) VALUES ('7', '100');
INSERT INTO `ialertdb`.`RELATED_USER` (`user_id`, `conf_level_thresh`) VALUES ('8', '100');
INSERT INTO `ialertdb`.`RELATED_USER` (`user_id`, `conf_level_thresh`) VALUES ('9', '100');
INSERT INTO `ialertdb`.`RELATED_USER` (`user_id`, `conf_level_thresh`) VALUES ('10', '100');

INSERT INTO `ialertdb`.`RELATED_USER_PICTURE` (`user_id`, `pic_id`, `pic_path`) VALUES ('1', '1', '../detected_faces_imgs/user1');
INSERT INTO `ialertdb`.`RELATED_USER_PICTURE` (`user_id`, `pic_id`, `pic_path`) VALUES ('2', '2', '../detected_faces_imgs/user2');
INSERT INTO `ialertdb`.`RELATED_USER_PICTURE` (`user_id`, `pic_id`, `pic_path`) VALUES ('3', '3', '../detected_faces_imgs/user3');
INSERT INTO `ialertdb`.`RELATED_USER_PICTURE` (`user_id`, `pic_id`, `pic_path`) VALUES ('4', '4', '../detected_faces_imgs/user4');
INSERT INTO `ialertdb`.`RELATED_USER_PICTURE` (`user_id`, `pic_id`, `pic_path`) VALUES ('5', '5', '../detected_faces_imgs/user5');
INSERT INTO `ialertdb`.`RELATED_USER_PICTURE` (`user_id`, `pic_id`, `pic_path`) VALUES ('6', '6', '../detected_faces_imgs/user6');
INSERT INTO `ialertdb`.`RELATED_USER_PICTURE` (`user_id`, `pic_id`, `pic_path`) VALUES ('7', '7', '../detected_faces_imgs/user7');
INSERT INTO `ialertdb`.`RELATED_USER_PICTURE` (`user_id`, `pic_id`, `pic_path`) VALUES ('8', '8', '../detected_faces_imgs/user8');
INSERT INTO `ialertdb`.`RELATED_USER_PICTURE` (`user_id`, `pic_id`, `pic_path`) VALUES ('9', '9', '../detected_faces_imgs/user9');
INSERT INTO `ialertdb`.`RELATED_USER_PICTURE` (`user_id`, `pic_id`, `pic_path`) VALUES ('10', '10', '../detected_faces_imgs/user10');


