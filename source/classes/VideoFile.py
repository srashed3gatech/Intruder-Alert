class VideoFile:
    
    def __init__(self, video_id, time_created, duration_sec, video_path, framerate, expiry):
        self.video_id = video_id
        self.time_created = time_created
        self.duration_sec = duration_sec
        self.video_path = video_path
        self.framerate = framerate
        self.expiry = expiry
        
    def __repr__(self):
        return "<VideoFile(video_id: %s, time_created: %s, duration_sec: %s, video_path: %s, framerate: %s, expiry: %s)>" % (self.video_id, self.time_created, self.duration_sec, self.video_path, self.framerate, self.expiry)
