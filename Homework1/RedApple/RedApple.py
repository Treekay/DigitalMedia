from PIL import Image
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

    # save the new img
    cv2.imwrite("../img/hw2.jpg",img)

    # show and compare
    cv2.imshow("RedApple", cv2.imread('../img/redapple.jpg'))
    cv2.imshow("AfterProcess", cv2.imread('../img/hw2.jpg'))
    cv2.waitKey(0)
    ###press 'ESC' to exit

# main()
ImgProcess(cv2.imread('../img/redapple.jpg'))