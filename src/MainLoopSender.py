import VideoSources
import VideoSinks
import cv2
import numpy as np
from FrameProcessors import Dither,SHARPEN,Filter,Interlacer,UnInterlace
import helper
import time



videoSource = VideoSources.CV2WebCamSource("Test",0)
videoSource.start()

videoSinkInterlaced = VideoSinks.CV2VideoSink("Interlaced")
videoSink = VideoSinks.CV2VideoSink("Test")

frameCount = 0
out = np.zeros((192,256))
while(True):
    frame = videoSource.getFrame()
    frame = cv2.resize(frame, (256,192)) 
    time.sleep(0.01)
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = Filter(gray,SHARPEN)
    gray =Dither(gray,10) 
    #print frameCount
    lines = Interlacer(gray,frameCount)
    #print lines.shape
    
    out = UnInterlace(out,lines,frameCount)
    
    frameCount +=1
    if frameCount == 3:
        frameCount = 0
   
    
    videoSinkInterlaced.writeFrame(out)
    videoSink.writeFrame(gray)
        
        
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        
        break
    
    
    
# When everything done, release the capture
videoSource.stop()

cv2.destroyAllWindows()