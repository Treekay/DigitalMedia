from PIL import Image
import math
import numpy as np
import matplotlib.pyplot as plt
import operator

def ImgProcess(img):
    rows, cols, dims = img.shape
    R, G, B = 0, 1, 2
    pixels = []

    # pick up all the pixels
    for x in range(rows):
        for y in range(cols):
            pixels.append([img[x,y,R],img[x,y,G],img[x,y,B]])

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

    newImg = img
    region = len(pixels)//256
    for t in range(256):
        medianColor = pixels[(2*t+1)*region//2]
        for i in range((t+1)*region):
            for x in range(rows):
                for y in range(cols):
                    if (newImg[x,y,R] == pixels[i][R] and
                        newImg[x,y,G] == pixels[i][G] and
                        newImg[x,y,G] == pixels[i][G]):
                        newImg[x,y,R] = medianColor[R]
                        newImg[x,y,G] = medianColor[G]
                        newImg[x,y,B] = medianColor[B]
            #pixels[i] = medianColor

    # show and save the new img
    img = Image.fromarray(np.uint8(newImg))
    plt.figure(2)
    plt.imshow(img)
    plt.axis('off')
    plt.show()
    plt.savefig("../img/hw2.jpg")

# main()
image = Image.open('../img/redapple.jpg')
img = np.array(image)
plt.figure(1)
plt.imshow(img)
plt.axis('off')
ImgProcess(img)