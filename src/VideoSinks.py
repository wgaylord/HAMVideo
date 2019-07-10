import cv2
import numpy as np
import struct
import helper
import zmq

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
        
        
        
        
class CV2VideoSink(VideoSink):
    def __init__(self,name):
        self.name = name + "-CV2"
        pass
        
    def writeFrame(self,frame):
        cv2.imshow(self.name,frame)
        
    def getName(self):
        return self.name
        
        
    def stop(self):
        cv2.destroyAllWindows() #Only kill this window?
        
        
        
class ZMQVideoSink(VideoSink):
    def __init__(self,name,addr,port):
        self.name = name + "-ZMQSink"
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind("tcp://"+addr+":%s" % port)

        
    def writeFrame(self,frame):
        self.socket.send(np.packbits(frame/255))
        
    def writeLines(self,lines,number):
        temp = np.packbits(lines/255)
        temp[0] = number
        self.socket.send(struct.pack("B"*2048,*temp))
        #self.sock.sendto(struct.pack("B"*2048,*temp), (self.addr , self.port))
        
    def getName(self):
        return self.name
        
        
    def stop(self):
        self.sock.close()
