from PIL import Image
import operator
import numpy as np
import matplotlib.pyplot as plt
import cv2
import sys

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

    
    # save the new img
    cv2.imwrite("../res/hw2.jpg",img)

    # show and compare
    cv2.imshow("RedApple", cv2.imread('../img/redapple.jpg'))
    cv2.imshow("AfterProcess", cv2.imread('../res/hw2.jpg'))
    cv2.waitKey(0)
    ###press 'ESC' to exit


    '''
    height, width, channels = img.shape
    # 去除坐标系
    plt.axis('off')
    # 去除图像周围的白边  
    fig, ax = plt.subplots()
    plt.figure(figsize=(6,4))
    fig.set_size_inches(width/100.0/3.0, height/100.0/3.0)  
    plt.gca().xaxis.set_major_locator(plt.NullLocator()) 
    plt.gca().yaxis.set_major_locator(plt.NullLocator()) 
    plt.subplots_adjust(top=1,bottom=0,left=0,right=1,hspace=0,wspace=0) 
    plt.margins(0,0)
    plt.imshow(Image.fromarray(img))
    # save
    plt.savefig('../res/hw2.jpg', dpi=300)
    plt.show()
    '''

# main()
f1 = open("../res/np.txt",'a')
f1.write(str(np.array(Image.open('../img/redapple.jpg'))))
f1.close()

f2 = open("../res/cv.txt",'a')
f2.write(str(cv2.imread('../img/redapple.jpg')))
f2.close()

ImgProcess(cv2.imread('../img/redapple.jpg'))