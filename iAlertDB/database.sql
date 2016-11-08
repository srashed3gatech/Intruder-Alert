CREATE SCHEMA `ialertdb` ;

USE ialertdb;

--
-- Table structure for table `USER`
--

DROP TABLE IF EXISTS `USER`;
CREATE TABLE `USER` (
  `user_id` varchar(15) NOT NULL,
  `name` varchar(45) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `SYSTEM_USER`
--

DROP TABLE IF EXISTS `SYSTEM_USER`;
CREATE TABLE `SYSTEM_USER` (
  `user_id` varchar(15) NOT NULL,
  `email` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL DEFAULT 'password',
  PRIMARY KEY (`user_id`),
  CONSTRAINT `fk_system_user_id` FOREIGN KEY (`user_id`) REFERENCES `USER` (`user_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


--
-- Table structure for table `VIDEO`
--

DROP TABLE IF EXISTS `VIDEO`;
CREATE TABLE `VIDEO` (
  `video_id` int(11) NOT NULL AUTO_INCREMENT,
  `time_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `duration_sec` double NOT NULL,
  `video_path` varchar(255) NOT NULL,
  `framerate` int(11) NOT NULL DEFAULT '30',
  `expiry` datetime NOT NULL,
  PRIMARY KEY (`video_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `SYSTEM_INFO`
--

DROP TABLE IF EXISTS `SYSTEM_INFO`;
CREATE TABLE `SYSTEM_INFO` (
  `key` varchar(255) NOT NULL,
  `value` varchar(255) NOT NULL,
  PRIMARY KEY (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `RELATED_USER`
--

DROP TABLE IF EXISTS `RELATED_USER`;
CREATE TABLE `RELATED_USER` (
  `user_id` varchar(15) NOT NULL,
  `conf_level_thresh` decimal(3,0) NOT NULL,
  PRIMARY KEY (`user_id`),
  CONSTRAINT `fk_related_user_id` FOREIGN KEY (`user_id`) REFERENCES `USER` (`user_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `RELATED_USER_PICTURE`
--

DROP TABLE IF EXISTS `RELATED_USER_PICTURE`;
CREATE TABLE `RELATED_USER_PICTURE` (
  `user_id` varchar(15) NOT NULL,
  `pic_id` int(11) NOT NULL,
  `pic_path` varchar(256) NOT NULL,
  PRIMARY KEY (`user_id`,`pic_id`),
  CONSTRAINT `fk_related_user_id_picture` FOREIGN KEY (`user_id`) REFERENCES `USER` (`user_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `FRAME`
--

DROP TABLE IF EXISTS `FRAME`;
CREATE TABLE `FRAME` (
  `video_id` int(11) NOT NULL,
  `frame_num` bigint(100) NOT NULL,
  `timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`video_id`,`frame_num`),
  CONSTRAINT `fk_frame_videoid` FOREIGN KEY (`video_id`) REFERENCES `VIDEO` (`video_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `CORRESPONDS_TO`
--

DROP TABLE IF EXISTS `CORRESPONDS_TO`;
CREATE TABLE `CORRESPONDS_TO` (
  `user_id` varchar(15) NOT NULL,
  `video_id` int(11) NOT NULL,
  `frame_num` bigint(100) unsigned NOT NULL,
  `conf_level` double NOT NULL,
  `face_num` int(11) DEFAULT NULL,
  PRIMARY KEY (`user_id`,`video_id`,`frame_num`),
  KEY `fk_corr_videoid_idx` (`video_id`),
  KEY `fk_corr_framenum_idx` (`frame_num`),
  CONSTRAINT `fk_corr_userid` FOREIGN KEY (`user_id`) REFERENCES `USER` (`user_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_corr_videoid_frameid` FOREIGN KEY (`video_id`) REFERENCES `FRAME` (`video_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `ALARM_CATEGORY`
--

DROP TABLE IF EXISTS `ALARM_CATEGORY`;
CREATE TABLE `ALARM_CATEGORY` (
  `cate_name` varchar(45) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`cate_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `CONFIGS`
--

DROP TABLE IF EXISTS `CONFIGS`;
CREATE TABLE `CONFIGS` (
  `user_id` varchar(15) NOT NULL,
  `cate_name` varchar(45) NOT NULL,
  `deferral_time_sec` int(11) NOT NULL DEFAULT '60',
  PRIMARY KEY (`user_id`,`cate_name`),
  KEY `fk_config_alarm_category_idx` (`cate_name`),
  CONSTRAINT `fk_config_alarm_category` FOREIGN KEY (`cate_name`) REFERENCES `ALARM_CATEGORY` (`cate_name`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_config_user_id` FOREIGN KEY (`user_id`) REFERENCES `USER` (`user_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `ALARM`
--

DROP TABLE IF EXISTS `ALARM`;
CREATE TABLE `ALARM` (
  `alarm_id` int(11) NOT NULL AUTO_INCREMENT,
  `first_occ` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `tally` int(11) NOT NULL DEFAULT '0',
  `clear_time` datetime DEFAULT NULL,
  `cate_name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`alarm_id`),
  KEY `fk_category_name_idx` (`cate_name`),
  CONSTRAINT `fk_category_name` FOREIGN KEY (`cate_name`) REFERENCES `ALARM_CATEGORY` (`cate_name`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `GENERATED_FROM`
--

DROP TABLE IF EXISTS `GENERATED_FROM`;
CREATE TABLE `GENERATED_FROM` (
  `video_id` int(11) NOT NULL,
  `frame_num` bigint(100) NOT NULL,
  `alarm_id` int(11) NOT NULL,
  PRIMARY KEY (`video_id`,`frame_num`),
  KEY `fk_genfrom_frameno_idx` (`frame_num`),
  KEY `fk_genfrom_alarmid_idx` (`alarm_id`),
  CONSTRAINT `fk_genfrom_alarmid` FOREIGN KEY (`alarm_id`) REFERENCES `ALARM` (`alarm_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_genfrom_frameno` FOREIGN KEY (`video_id`, `frame_num`) REFERENCES `FRAME` (`video_id`, `frame_num`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


--
-- Table structure for table `SENT_TO`
--

DROP TABLE IF EXISTS `SENT_TO`;
CREATE TABLE `SENT_TO` (
  `user_id` varchar(15) NOT NULL,
  `alarm_id` int(11) NOT NULL,
  `status` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`user_id`,`alarm_id`),
  KEY `fk_sentto_alarmid_idx` (`alarm_id`),
  CONSTRAINT `fk_sentto_alarmid` FOREIGN KEY (`alarm_id`) REFERENCES `ALARM` (`alarm_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_sentto_userid` FOREIGN KEY (`user_id`) REFERENCES `USER` (`user_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;