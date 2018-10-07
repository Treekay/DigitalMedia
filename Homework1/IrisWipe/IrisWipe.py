from PIL import Image
import numpy as np
import math

def IrisWipe(img1, img2):
    im1 = np.array(img1)
    im2 = np.array(img2)
    rows, cols, dims = im1.shape

    # initial
    t = 0
    frames = []
    while t < 11:
        # the radius decide by the time
        r = 40*t
        for x in range(cols):
            for y in range(rows):
                if (pow(x-rows//2-1,2)+pow(y-rows//2-1,2)<=pow(r,2)):
                    # change the circle region to lena
                    im1[x,y] = im2[x,y]
        t += 1
        # append the temp img
        frames.append(im1)

    # create a gif
        frames[0].save('../res/IrisWipe.gif', )
    # Show the gif
        

# main()
img1 = Image.open('../img/Nobel.jpg')
img2 = Image.open('../img/lena.jpg')
IrisWipe(img1, img2)