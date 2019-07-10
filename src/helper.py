from amodem import framing
import numpy as np
from amodem import send

        
class DoNothing:
    '''Custom Checksum'''
    
    def encode(self, payload):
        return payload

    def decode(self, data):
        return data
        
 
class Sender:
    def __init__(self,config,dst,gain):
        self.framer = framing.Framer()
        self.framer.checksum = DoNothing()
        self.sender = send.Sender(dst, config=config, gain=gain)
        self.config = config
        self.Fs = config.Fs
       
    def start(self):
        self.sender.start()
       
    def send(self,data):
        #self.sender.start()
        self.sender.write(np.zeros(int(self.config.silence_start)))
        bits = framing.encode(data,self.framer)
        self.sender.modulate(bits=bits)
        
        
class Receiever:
    def __init__(self,config,dst,gain):
        pass
    