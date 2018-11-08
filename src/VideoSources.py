import numpy as np

from cv2 import VideoCapture,cvtColor,COLOR_BGR2GRAY,imread


class VideoSource:
    def __init__(self,name):
        self.name = name
        self.size = (0,0)
        pass
        
    def getFrame(self):
        return []
        
    def getSize(self):
        return self.size
        
    def getName(self):
        return self.name
    
    def getFPS(self):
        return 0
        
    def start(self):
        pass
        
    def stop(self):
        pass
        
        
        
class CV2WebCamSource(VideoSource):
    def __init__(self,name,camNumber):
        VideoSource.__init__(self,name+"-CV2Cam"+str(camNumber))
        self.camNumber = camNumber

                  
    def getFrame(self):
        ret, rawFrame = self.cap.read()
        return rawFrame
        
    def getFPS(self):
        return 28
        
    def start(self):
        self.cap = VideoCapture(self.camNumber)
        self.size = (int(self.cap.get(3)),int(self.cap.get(4)))
            
    def stop(self):
        self.cap.release()
        
class StillImageSource(VideoSource):
    def __init__(self,name,fileName):
        VideoSource.__init__(self,name+"-StillImageSource-"+fileName)
        self.fileName = fileName
        self.image = None
                  
    def getFrame(self):
        return self.image
        
    def getFPS(self):
        return 0
        
    def start(self):
        self.image = imread(self.fileName)
            
    