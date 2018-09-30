from PIL import Image
import math
import numpy as np
import matplotlib.pyplot as plt

img = np.array(Image.open('../img/redapple.jpg'))
rows, cols, dims = img.shape

plt.imshow(img)
plt.pause(2)

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

# statistics the num of each r,g,b
for i in range(pixels.size()):
    channel[R][pixels[i][R]] += 1
    channel[G][pixels[i][G]] += 1
    channel[B][pixels[i][B]] += 1

# get the ColorNumTuple
tube = [[],[],[]]
for i in range(3):
    for t in range(channel[i].size()):
        if (channel[i][t] != 0):
            tube[i].append(tuple(t,channel[i][t]))

sorted(tube[R], key=lambda tube[R] : tube[R][1])
sorted(tube[G], key=lambda tube[G] : tube[G][1])
sorted(tube[B], key=lambda tube[B] : tube[B][1])

def divideByRchannel(tubes):
    