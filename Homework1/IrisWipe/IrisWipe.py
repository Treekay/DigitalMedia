from PIL import Image
import numpy as np
import os
import math

def IrisWipe(img1, img2):
    im1 = np.array(img1)
    im2 = np.array(img2)
    rows, cols, dims = im1.shape

    # initial
    r = 0
    frames = []
    print("Creating...")
    while r <= 580:
        for x in range(cols):
            for y in range(rows):
                if (pow(x - rows // 2 - 1,2) + pow(y - rows // 2 - 1,2) <= pow(r, 2)):
                    # change the circle region to lena
                    im1[x,y] = im2[x,y]
        r += 15
        # append the temp img
        frames.append(Image.fromarray(im1))

    # create a gif
    frames[0].save('./img/hw1.gif', save_all = True, append_images = frames[1:], duration = 0.01, loop = 0)
    # Show the gif
    os.system(r"start ./img/hw1.gif")
    print("Success")

# main()
img1 = Image.open('./img/Nobel.jpg')
img2 = Image.open('./img/lena.jpg')
IrisWipe(img1, img2)