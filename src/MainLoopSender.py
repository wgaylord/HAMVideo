import VideoSources
import VideoSinks
import cv2
import numpy as np
from FrameProcessors import Dither,SHARPEN,Filter,Interlacer,UnInterlace,AddCall


CALLSIGN = "KD9KCK"


videoSource = VideoSources.CV2WebCamSource("Test",0)
videoSource.start()

videoSinkInterlaced = VideoSinks.CV2VideoSink("Interlaced")


UDPVideo = VideoSinks.ZMQVideoSink("Test","0.0.0.0",5001)

frameCount = 0



while(True):
    frame = videoSource.getFrame()
    frame = cv2.resize(frame, (256,192)) 
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = Filter(gray,SHARPEN)
    gray =Dither(gray,10) 
    gray = AddCall(gray,CALLSIGN)
    #print frameCount
    lines = Interlacer(gray,frameCount)
    #print lines.shape
    UDPVideo.writeLines(lines,frameCount)
    #AModem.writeLines(lines,frameCount)
    #AModem.writeFrame(gray)
    frameCount+=1
    
    if frameCount > 2:
        frameCount = 0
   
    
    videoSinkInterlaced.writeFrame(gray)
        
    
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        stream.close()
        break
    
    
    
# When everything done, release the capture
videoSource.stop()

cv2.destroyAllWindows()