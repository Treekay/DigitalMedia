from PIL import Image
import math
import numpy as np
import matplotlib.pyplot as plt
import cv2

def IrisWipe(img1, img2):
    im1 = np.array(img1)
    im2 = np.array(img2)
    rows, cols, dims = im1.shape

    # initial
    increment = cols//10
    centre = cols//2-1
    t = 0
    while t < 20:
        # the radius decide by the time
        r = 40*t

        lowbound = centre-increment*t
        upbound = centre+increment*t
        if (lowbound < 0):
            lowbound = 0
        if (upbound > cols - 1):
            upbound = cols - 1

        for x in range(lowbound,upbound):
            for y in range(lowbound,upbound):
                if (pow(x-centre,2)+pow(y-centre,2)<=pow(r,2)):
                    # change the circle region to lena
                    im1[x,y] = im2[x,y]
        t += 1
        plt.imshow(im1)
        plt.axis('off') # 去除坐标系
        # keep a while show the changing process
        plt.pause(0.03)
    plt.close()

# main()
img1 = Image.open('../img/Nobel.jpg')
img2 = Image.open('../img/lena.jpg')
IrisWipe(img1, img2)