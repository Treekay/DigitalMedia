import cv2
import numpy as np

import JpegCompress
import JpegDecompress

# 计算压缩率
def computeCompressionRatio():
    pass

# 计算失真度
def computeDistortionRatio(srcPath, resPath):
    src = cv2.imread(srcPath)
    res = cv2.imread(resPath)
    MSE = np.mean(np.square(src- res))
    print('MSE: %f' % MSE)

if __name__ == "__main__":
    # test1
    compress1 = JpegCompress.Compress('./src/cartoon.jpg')
    compressedData1 = compress1.getCompressedData()
    decompress1 = JpegDecompress.Decompress(compressedData1, './res/cartoon.png')
    compressedImg1 = decompress1.getDecompressImg()
    computeDistortionRatio('./src/cartoon.jpg', './res/cartoon.png')
    # test2
    compress2 = JpegCompress.Compress('./src/animal.jpg')
    compressedData2 = compress2.getCompressedData()
    decompress2 = JpegDecompress.Decompress(compressedData2, './res/animal.png')
    compressedImg2 = decompress2.getDecompressImg()
    computeDistortionRatio('./src/animal.jpg', './res/animal.png')
