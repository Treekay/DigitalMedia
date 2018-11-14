#JPEG compression algorithm
import numpy as np
from PIL import Image

'''
@msg: compress jpeg-format image
@param srcPath: the source image path
@param resPath: the result image path
'''
def Compression(srcPath, resPath):
    #load img
    img = np.array(Image.open(srcPath))
    rows, cols, dims = img.shape

    # color space conversion: RGB -> YCbCr
    YUVimg = img
    for x in range(cols):
        for y in range(rows):
            R = img[x, y, 0]
            G = img[x, y, 1]
            B = img[x, y, 2]
            YUVimg[x, y, 0] = 0.299 * R + 0.587 * G + 0.144 * B
            YUVimg[x, y, 1] = -0.1687 * R - 0.3313 * G + 0.5 * B + 128
            YUVimg[x, y, 2] = 0.5 * R + 0.418 * G - 0.0813 * B + 128
    # chroma double sampling
    
    # 2D-DCT transform

    # quantization

    # DPCM

    # RLC

    # entropy coding

    #save img
    img = Image.fromarray(img)
    img.save(resPath)

if __name__ == "__main__":
    Compression('./src/cartoon.jpg', './res/cartoon.jpg')
    Compression('./src/reality.jpg', './res/reality.jpg')
