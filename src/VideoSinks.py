import cv2

class VideoSink:
    def __init__(self,name):
        self.name = name
        pass
        
    def writeFrame(self,frame):
        pass
        
    def getName(self):
        return self.name
        
    def start(self):
        pass
        
    def stop(self):
        pass
        
        
        
        
class CV2VideoSink:
    def __init__(self,name):
        self.name = name + "-CV2"
        pass
        
    def writeFrame(self,frame):
        cv2.imshow(self.name,frame)
        
    def getName(self):
        return self.name
        
        
    def stop(self):
        cv2.destroyAllWindows() #Only kill this window?
        
        
        
class FileSink:
    def __init__(self,name,filename):
        self.name = name
        pass
        
    def writeFrame(self,frame):
        pass
        
    def getName(self):
        return self.name
        
    def start(self):
        pass
        
    def stop(self):
        pass
        