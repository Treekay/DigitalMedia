from PIL import Image
import numpy as np
import copy
import time

def findMinEdistancePos(a,b):
    return np.argmin(np.sqrt(np.sum(np.asarray(a-b)**2, axis=1)))

def ImgProcess(img):
    R, G, B = 0, 1, 2
    dim1, dim2, dim3 = img.shape
    img = np.reshape(img,(-1,3))
    pixels = copy.deepcopy(img)

    # sort the pixels color
    medianPos = len(pixels)
    for t in range(8):
        ltimes = len(pixels)//medianPos
        for i in range(ltimes):
            temp = pixels[i*medianPos:(i+1)*medianPos]
            pixels[i*medianPos:(i+1)*medianPos] = temp[np.lexsort(temp.T[t%3,None])]
        medianPos = medianPos//2

    # create the LUT
    regionLen = len(pixels)//256
    LUT = []
    for i in range(256):
        LUT.append(np.rint(np.mean(pixels[i*regionLen:(i+1)*regionLen-1],axis=0)).tolist())
    np.array(LUT)

    # process the img
    for i in range(len(img)):
        img[i] = LUT[findMinEdistancePos(img[i],LUT)]
    img = np.reshape(img,(dim1,dim2,dim3))
    

    # save the new img
    im = Image.fromarray(img)
    im.save("./img/hw2.jpg")

    # show and compare
    Image.open('./img/hw2.jpg').show(title="AfterProcess")
    ###press 'ESC' to exit

# main()

print("Processing...")
time_start=time.time()

ImgProcess(np.array(Image.open('./img/redapple.jpg')))
print("Finish!")

time_end=time.time()
print("cost time:",int(time_end-time_start),"seconds")