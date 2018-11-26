import cv2
import numpy as np

import JpegCompress
import JpegDecompress

# 计算压缩率
def computeCompressionRatio(srcPath, compressed):
    src = cv2.imread(srcPath)
    rows, cols, dims = src.shape
    pixels = rows * cols * dims
    data = pixels * 8

    dc = compressed[0]
    ac = compressed[1]
    compressData = 0
    for t in range(3):
        compressData += 4 * 8 * len(dc[t]) + 4 * 8 * len(ac[t])

    ratio = compressData / data
    print("Compression Ratio: %f" % ratio)

# 计算失真度
def computeDistortionRatio(srcPath, resPath):
    src = cv2.imread(srcPath)
    res = cv2.imread(resPath)
    MSE = np.mean(np.square(src- res))
    print('MSE: %f' % MSE)

    SNR = 10 * np.log10(np.mean(np.square(src - np.mean(src))) / MSE)
    print('SRN: %f' % SNR)

    PSNR = 10 * np.log10(np.max(np.square(src)) / MSE)
    print('PSNR: %f' % PSNR)

if __name__ == "__main__":
    # test1
    compress1 = JpegCompress.Compress('./src/cartoon.jpg')
    compressedData1 = compress1.getCompressedData()
    computeCompressionRatio('./src/cartoon.jpg', compressedData1)

    decompress1 = JpegDecompress.Decompress(compressedData1, './res/cartoon.png')
    compressedImg1 = decompress1.getDecompressImg()
    computeDistortionRatio('./src/cartoon.jpg', './res/cartoon.png')

    # test2
    compress2 = JpegCompress.Compress('./src/animal.jpg')
    compressedData2 = compress2.getCompressedData()
    computeCompressionRatio('./src/animal.jpg', compressedData2)

    decompress2 = JpegDecompress.Decompress(compressedData2, './res/animal.png')
    compressedImg2 = decompress2.getDecompressImg()
    computeDistortionRatio('./src/animal.jpg', './res/animal.png')
