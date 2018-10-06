from PIL import Image
import math
import numpy as np
import matplotlib.pyplot as plt
import operator
import cv2

def ImgProcess(img):
    rows, cols, dims = img.shape
    R, G, B = 0, 1, 2
    pixels = []

    # pick up all the pixels
    for x in range(rows):
        for y in range(cols):
            pixels.append([img[x,y,R],img[x,y,G],img[x,y,B],x,y])

    # determine the 256 present color
    medianNum = len(pixels)
    pixels.sort(key=operator.itemgetter(R))
    for t in range(8):
        medianNum = medianNum//2
        ltimes = len(pixels) // medianNum
        if (t%3 == 0):
            for i in range(ltimes):
                pixels[i*medianNum:(i+1)*medianNum].sort(key=operator.itemgetter(R))
        elif (t%3 == 1):
            for i in range(ltimes):
                pixels[i*medianNum:(i+1)*medianNum].sort(key=operator.itemgetter(G))
        elif (t%3 == 2):
            for i in range(ltimes):
                pixels[i*medianNum:(i+1)*medianNum].sort(key=operator.itemgetter(B))

    region = len(pixels)//256
    for t in range(256):
        medianColor = pixels[(2*t+1)*region//2]
        for i in range(t*region,(t+1)*region):
            x = pixels[i][3]
            y = pixels[i][4]
            img[x,y,R] = medianColor[R]
            img[x,y,G] = medianColor[G]
            img[x,y,B] = medianColor[B]

    height, width, channels = img.shape
    # 去除坐标系
    fig, ax = plt.subplots() 
    plt.axis('off')
    # 去除白边
    fig.set_size_inches(width/100.0/3.0, height/100.0/3.0)  
    plt.gca().xaxis.set_major_locator(plt.NullLocator()) 
    plt.gca().yaxis.set_major_locator(plt.NullLocator()) 
    plt.subplots_adjust(top=1,bottom=0,left=0,right=1,hspace=0,wspace=0) 
    plt.margins(0,0)

    # save the new img
    img = Image.fromarray(np.uint8(img))
    plt.imshow(img)
    plt.savefig("../img/hw2.jpg",dpi=300)

# main()
img = np.array(Image.open('../img/redapple.jpg'))
ImgProcess(img)

# show the new img
cv2.imshow("RedApple", cv2.imread('../img/redapple.jpg'))
cv2.imshow("AfterProcess", cv2.imread('../img/hw2.jpg'))
cv2.waitKey(0)