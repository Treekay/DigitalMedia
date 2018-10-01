from PIL import Image
import math
import numpy as np
import matplotlib.pyplot as plt

def findMedian(tubes,medianNum):
    for i in range(len(tubes)):
        if (medianNum-tubes[i][1]<=0):
            return int(tubes[i][0])
        else: medianNum -= tubes[i][1]

img = np.array(Image.open('../img/redapple.jpg'))
rows, cols, dims = img.shape

#plt.imshow(img)
#plt.pause(2)

# pick up all the pixels
pixels = []
for x in range(rows):
    for y in range(cols):
        pixels.append(img[x,y,:])

# initial
channel = [[],[],[]]
R, G, B = 0, 1, 2
for i in range(256):
    channel[R].append(0)
    channel[G].append(0)
    channel[B].append(0)

print(len(pixels))
# statistics the num of each r,g,b
for i in range(len(pixels)):
    channel[R][pixels[i][R]] += 1
    channel[G][pixels[i][G]] += 1
    channel[B][pixels[i][B]] += 1

# get the ColorNumTuple
tube = [[],[],[]]
for i in range(3):
    for t in range(len(channel[i])):
        if (channel[i][t] != 0):
            tube[i].append([t,channel[i][t]])

print(tube[R],'\n',tube[G],'\n',tube[B])
medianNum = len(pixels)//2

print(findMedian(tube[R],medianNum),findMedian(tube[G],medianNum),findMedian(tube[B],medianNum))