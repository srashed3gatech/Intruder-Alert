'''This is responsible for:
    - read all related users from DBUtitity.get_realted_users
    - train and generate face_recognizer.xml at startup'''
class BootLoader():
    def __init__(self, userListTrain):
        self.userList = userListTrain
    
    def trainModel(self):
        '''1. Read pic path from userList
           2. create and return face_recognizer.xml file path
        '''
        #if userList empty - then create a default face recognizer and send it 
        
        return "../face_recognizer.xml"