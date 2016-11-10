class VideoFrame:
    
    def __init__(self, videoId, frameNum, timestamp, userId, confidLevel):
        self.video_id = videoId
        self.frame_num = frameNum
        self.timestamp = timestamp
        self.user_id = userId
        self.confid_level = confidLevel
