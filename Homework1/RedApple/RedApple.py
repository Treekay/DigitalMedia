from PIL import Image
import time
import math
import numpy as np
import matplotlib.pyplot as plt

def statistics(channel):
    pixels = []
    for i in range(255):
        pixels[i+1] = (i+1,0)
    for pix in channel:
        pixels[pix] += 1
    return pixels

img = np.array(Image.open('../img/redapple.jpg'))
rows, cols, dims = img.shape
# pick up each color channel    
Rchannel = list(img[x,y,0]).sort()
Gchannel = list(img[x,y,1]).sort()
Bchannel = list(img[x,y,2]).sort()
# statistics r,g,b of pixels
Rpixels = statistics(Rchannel)
Gpixels = statistics(Gchannel)
Bpixels = statistics(Bchannel)

front = 0
back = Rpixels.size() - 1
for i in range(8):
    median = (front+back)//2
    # Red for 3 times
    if i%3==0:
        for t in range(front,median):

    # Green for 3 times
    elif i%3==1:

    # Blue for 2 times
    else:
