import cv2
import numpy as np
from PIL import Image

import JpegCompress
import JpegDecompress

# 计算失真度
def computeDistortionRatio(src, res):
    MSE = np.mean(np.square(src- res))
    print('MSE: %f' % MSE)

if __name__ == "__main__":
    # test1
    src1 = cv2.imread('./src/cartoon.bmp')
    # JPEG压缩图像
    compress1 = JpegCompress.Compress(src1)
    compressedData1 = compress1.getCompressedData()
    # 将压缩结果解码为无损格式图像(若存为jpg格式得到的是二次压缩的压缩结果)
    decompress1 = JpegDecompress.Decompress(compressedData1, './res/cartoon.jpg')
    compressedImg1 = decompress1.getDecompressImg()
    computeDistortionRatio(src1, compressedImg1)
    gif1 = np.array(Image.open("./res/cartoon.gif").convert('RGB'))[..., ::-1]
    computeDistortionRatio(src1, gif1)

    # test2
    src2 = cv2.imread('./src/animal.bmp')
    # JPEG压缩图像
    compress2 = JpegCompress.Compress(src2)
    compressedData2 = compress2.getCompressedData()
    # 将压缩结果解码为无损格式图像(若存为jpg格式得到的是二次压缩的压缩结果)
    decompress2 = JpegDecompress.Decompress(compressedData2, './res/animal.jpg')
    compressedImg2 = decompress2.getDecompressImg()
    computeDistortionRatio(src2, compressedImg2)
    gif2 = np.array(Image.open("./res/animal.gif").convert('RGB'))[..., ::-1]
    computeDistortionRatio(src2, gif2)