#JpegCompress.py
import cv2
import math
import numpy as np

class Decompress(object):
    def __init__(self, data, resPath):
        pass

    def __YCbCr2RGB(self):
        xform = np.array([[1, 0, 1.402], [1, -0.34414, -.71414], [1, 1.772, 0]])
        rgb = im.astype(np.float)
        rgb[:, :, [1, 2]] -= 128
        rgb = rgb.dot(xform.T)
        np.putmask(rgb, rgb > 255, 255)
        np.putmask(rgb, rgb < 0, 0)
        return np.uint8(rgb)
        
    # 熵解码器
    def __EntropyDecoding():
        pass

    # 反量化器

    # IDCT

    # 拼接成原图像

    def getDecompressImg(self):
        pass
