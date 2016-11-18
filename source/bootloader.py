from DBUtility import iAlertDB
import numpy as np
from PIL import Image
import cv2, sys, os
import logging
'''This is responsible for:
    - read all related users from DBUtitity.get_realted_users
    - train and generate face_recognizer.xml at startup
   NOTICE: 
    '''
class BootLoader():
    
    MODEL_PATH = "../face_recognizer.xml"
    
    def __init__(self, userListTrain):
        self.userList = userListTrain
        self.logger = logging.getLogger(__name__)
#         print self.userList
    
    '''
    Given a single-user pic dir and output images/labels 
    '''
    def _get_images_and_labels(self, path):
        ## Append all the absolute image paths in a list image_paths
        image_paths = [os.path.join(path, f) for f in os.listdir(path)]
        ## face images
        images = []
        ## labels
        labels = []
        for image_path in image_paths:
            ## Read the image and convert to grayscale
            image_pil = Image.open(image_path).convert('L')
            ## Convert the image format into numpy array
            image = np.array(image_pil, 'uint8')
            ## Get the label of the image
            nbr = int(os.path.split(path)[1].split(".")[0].replace("user", ""))
            images.append(image)
            labels.append(nbr)
            cv2.imshow("Adding faces to traning set...", image)
            cv2.waitKey(50)
        ## return the images list and labels list
        return images, labels
    
    def trainModel(self):
        '''1. Read pic path from userList
           2. create and return face_recognizer.xml file path
        '''
        #if userList empty - then create a default face recognizer and send it 
        if not self.userList:
            pass
        else:
            recognizer = cv2.createLBPHFaceRecognizer()
            images = []
            labels = []
            for u in self.userList:
                imgs, lbls = self._get_images_and_labels(u.pic_path)
                images = images + imgs
                labels = labels + lbls
            cv2.destroyAllWindows()
            recognizer.train(images, np.array(labels))
            recognizer.save(self.MODEL_PATH)
            print("Trained from Related_users and Saved model")
            self.logger.info("Trained from Related_users and Saved model - "+self.MODEL_PATH)
        return self.MODEL_PATH
    
if __name__ == "__main__":
    db = iAlertDB()
    bootLoader = BootLoader(db.get_realted_users())
    faceRecogXmlFilePath = bootLoader.trainModel()
    print faceRecogXmlFilePath
