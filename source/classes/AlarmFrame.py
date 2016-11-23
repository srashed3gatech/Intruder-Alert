class AlarmFrame:
    
    def __init__(self, alarmid, alarm_category, 
                 first_occ, last_occ, tally, clear_time,
                 videoId, videoFile, frameNum):
        self.alarmid = alarmid
        self.alarm_cateogry = alarm_category
        self.first_occ = first_occ
        self.last_occ = last_occ
        self.tally = tally
        self.clear_time = clear_time
        self.video_id = videoId 
        self.video_file = videoFile
        self.frame_num = frameNum #this is a list of frames
        
    def __repr__(self):
        return "<AlarmFrame(alarmid: %s, alarm_category: %s, first_occ: %s, last_occ: %s, tally: %s, clear_time: %s, video_id: %s, video_file: %s, frameNum: %s)>" % (self.alarmid, self.alarm_category, self.first_occ, self.last_occ, self.tally, self.clear_time, self.video_id, self.video_file, self.frameNum)
