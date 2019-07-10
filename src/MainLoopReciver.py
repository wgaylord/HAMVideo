import VideoSources
import VideoSinks
import cv2
import numpy as np
from FrameProcessors import UnInterlace
import helper
import struct
import zmq


videoSinkInterlaced = VideoSinks.CV2VideoSink("Interlaced")


frameCount = 0
out = np.zeros((192,256))
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect ("tcp://127.0.0.1:5001")
socket.setsockopt(zmq.SUBSCRIBE, "")
while(True):
    data = socket.recv()
    #print len(data),len(data[10:])
    data = struct.unpack("B"*2048,data)
    #print data[7:]
    frameCount = data[0]
    
    lines = np.unpackbits(np.asarray(data,dtype=np.uint8))
    #print lines
    lines.shape = (64,256)
    #print lines
    out = UnInterlace(out,lines,frameCount)
    videoSinkInterlaced.writeFrame(out*255)

        
        
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        
        break
    
    
    
# When everything done, release the capture
videoSource.stop()

cv2.destroyAllWindows()