import operator
import math
import cv2
import sys

def ImgProcess(img):
    rows, cols, dims = img.shape
    R, G, B = 2, 1, 0
    pixels = []

    # pick up all the pixels
    for x in range(rows):
        for y in range(cols):
            pixels.append([img[x,y,B],img[x,y,G],img[x,y,R],x,y])

    '''
    # determine the 256 present color
    medianPos = len(pixels)
    pixels.sort(key=operator.itemgetter(R))
    for t in range(8):
        medianPos = medianPos//2
        ltimes = len(pixels) // medianPos
        if (t%3 == 0):
            for i in range(ltimes):
                pixels[i*medianPos:(i+1)*medianPos].sort(key=operator.itemgetter(R))
        elif (t%3 == 1):
            for i in range(ltimes):
                pixels[i*medianPos:(i+1)*medianPos].sort(key=operator.itemgetter(G))
        elif (t%3 == 2):
            for i in range(ltimes):
                pixels[i*medianPos:(i+1)*medianPos].sort(key=operator.itemgetter(B))

    region = len(pixels)//256
    for t in range(256):
        presentColor = [[],[],[]]
        Rsum = 0
        Gsum = 0
        Bsum = 0
        for i in range(t*region,(t+1)*region):
            Rsum += pixels[i][R]
            Gsum += pixels[i][G]
            Bsum += pixels[i][B]
        presentColor[R] = Rsum // region
        presentColor[G] = Gsum // region
        presentColor[B] = Bsum // region
        for i in range(t*region,(t+1)*region):
            x = pixels[i][3]
            y = pixels[i][4]
            img[x,y,R] = presentColor[R]
            img[x,y,G] = presentColor[G]
            img[x,y,B] = presentColor[B]
    '''
    # save the new img
    cv2.imwrite("../res/hw2.jpg",img)

    # show and compare
    cv2.imshow("RedApple", cv2.imread('../img/redapple.jpg'))
    cv2.imshow("AfterProcess", cv2.imread('../res/hw2.jpg'))
    cv2.waitKey(0)
    ###press 'ESC' to exit

# main()
ImgProcess(cv2.imread('../img/redapple.jpg'))