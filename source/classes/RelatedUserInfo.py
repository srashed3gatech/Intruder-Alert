class RelatedUserInfo:
    
    def __init__(self, user_id, pic_id, pic_path, conf_level_thresh):
        self.user_id = user_id
        self.pic_id = pic_id
        self.pic_path = pic_path
        self.conf_level_thresh = conf_level_thresh
        
    def __repr__(self):
        return "<RelatedUserInfo(user_id: %s, pic_id: %s, pic_path: %s, conf_levl: %s)>" % (self.user_id, self.pic_id, self.pic_path, self.conf_level_thresh)