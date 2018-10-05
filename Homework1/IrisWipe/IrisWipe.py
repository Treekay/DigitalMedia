from PIL import Image
import math
import numpy as np
import matplotlib.pyplot as plt

# load the images and keep its data in np.array type
im1 = np.array(Image.open('../img/诺贝尔.jpg'))
im2 = np.array(Image.open('../img/lena.jpg'))
rows, cols, dims = im1.shape

# initial the counting time
t = 0
while t < 500:
    # check each pixel by rows and cols
    for x in range(rows):
        for y in range(cols):
            # the radius decide by the time
            if (pow(x-rows//2,2)+pow(y-cols//2,2)<=pow(t,2)):
                # change the circle region to lena.jpg 
                im1[x,y,:] = im2[x,y,:]
    t += 40
    plt.imshow(im1)
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=None) # 去除白边
    plt.axis('off') # 去除坐标系
    # keep a while show the changing process
    plt.pause(0.03)
plt.close()