import numpy as np
import numba
from numba import cuda
import cv2

SHARPEN = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
SMOOTH = np.ones((5,5),np.float32)/25

@numba.jit       
def Dither(num, thresh = 175):
    derr = np.zeros(num.shape, dtype=int)

    div = 8
    for y in xrange(num.shape[0]):
        for x in xrange(num.shape[1]):
            newval = derr[y,x] + num[y,x]
            if newval >= thresh:
                errval = newval - 255
                num[y,x] = 1.
            else:
                errval = newval
                num[y,x] = 0.
            if x + 1 < num.shape[1]:
                derr[y, x + 1] += errval / div
                if x + 2 < num.shape[1]:
                    derr[y, x + 2] += errval / div
            if y + 1 < num.shape[0]:
                derr[y + 1, x - 1] += errval / div
                derr[y + 1, x] += errval / div
                if y + 2< num.shape[0]:
                    derr[y + 2, x] += errval / div
                if x + 1 < num.shape[1]:
                    derr[y + 1, x + 1] += errval / div
    return np.flip((num[::-1,:] * 255),0).astype(np.uint8)

def Filter(frame,filter):
    return cv2.filter2D(frame, -1, filter)
    

@numba.jit     
def Dither2(img):
    img = img.astype('float32')
    h, w = img.shape
    for i in range(h):
        for j in range(w):
            cc = img[i, j]
            rc = (cc > 128) * 255
            err = cc - rc
            img[i, j] = rc
            if j + 1 < w:
                img[i, j+1] += err * 7/16
            if i + 1 == h:
                continue
            if j > 0:
                img[i+1, j-1] += err * 3/16
            img[i+1, j] += err * 5/16
            if j + 1 < w:
                img[i+1, j+1] += err * 1/16
    return img    
    
    
def Interlacer(frame,even):
    t = frame.shape[0]/3
    if even == 0:
        return frame[:t]
    if even == 1:
        return frame[t:t*2]
    if even == 2:
        return frame[t*2:]
    
    
    
    
def UnInterlace(frame,new_lines,even):
    t = frame.shape[0]/3
    if even == 0:
        frame[:t] = new_lines
        return frame
    if even == 1:
        frame[t:t*2] = new_lines
        return frame
    if even == 2:
        frame[t*2:] = new_lines
        return frame

