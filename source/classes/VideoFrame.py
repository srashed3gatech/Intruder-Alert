class VideoFrame:
    
    def __init__(self, videoId, frameNum, timestamp, userId, confidLevel):
        self.video_id = videoId
        self.frame_num = frameNum
        self.timestamp = timestamp
        self.user_id = userId
        self.confid_level = confidLevel
        
    def __repr__(self):
        return "<VideoFrame(user_id: %s, video_id: %s, timestamp: %s, confid_level: %s)>" % (self.user_id, self.video_id, self.timestamp, self.confid_level)
