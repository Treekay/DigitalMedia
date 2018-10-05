from PIL import Image
import math
import numpy as np
import matplotlib.pyplot as plt

def findMedian(tubes,medianNum):
    for i in range(len(tubes)):
        if (medianNum-tubes[i][1]<=0):
            return int(tubes[i][0])
        else: medianNum -= tubes[i][1]

def ImgProcess(img):
    rows, cols, dims = img.shape
    R, G, B = 0, 1, 2

    pixels = []
    # pick up all the pixels
    for x in range(rows):
        for y in range(cols):
            pixels.append(img[x,y,:])

    distribution = [[],[],[]]
    # initial and statistics the num of each channel
    for i in range(256):
        distribution[R].append(0)
        distribution[G].append(0)
        distribution[B].append(0)
    for i in range(len(pixels)):
        distribution[R][pixels[i][R]] += 1
        distribution[G][pixels[i][G]] += 1
        distribution[B][pixels[i][B]] += 1

    channel = [[],[],[]]
    # get the Color-Num Pairs
    for i in range(3):
        for t in range(256):
            if (distribution[i][t] != 0):
                channel[i].append([t,distribution[i][t]])

    # determine the 256 present color
    R1 = [[],[]]
    # Loop1: R
    medianNum = len(pixels)
    for t in range(8):
        medianNum = medianNum//2
        ltimes = pixels // medianNum
        if (t%3 == 0):
            for i in range(ltimes):
                for index in range(channel[R][i*medianNum:(i+1)*medianNum]):

        elif (t%3 == 1):
        elif (t%3 == 2):

    # show and save the new img
    

# main()
img = np.array(Image.open('../img/redapple.jpg'))
ImgProcess(img)