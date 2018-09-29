from PIL import Image
import time
import math
import numpy as np
import matplotlib.pyplot as plt

im1 = np.array(Image.open('../img/诺贝尔.jpg'))
im2 = np.array(Image.open('../img/lena.jpg'))

rows, cols, dims = im1.shape

img = im1
t = 0
while t < 500:
    drawRange = {}
    for x in range(rows):
        for y in range(cols):
            if (pow(int(x-rows/2),2)+pow(int(y-cols/2),2)<=pow(t,2)):
                img[x,y,:] = im2[x,y,:]
    t += 40
    plt.imshow(img)
    plt.pause(0.03)
plt.close()