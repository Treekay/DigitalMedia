#JpegCompress.py
import cv2

from utils import *

class Compress(object):
    def __init__(self, srcPath):
        # load image
        self.__BGRimg = cv2.imread(srcPath)
        self.__height, self.__width, self.__dim = self.__BGRimg.shape
        self.__RGBimg = self.__BGRimg[:, :, : : -1]
        # do compress
        self.__RGB2YCbCr()
        self.__DoubleSampling()
        self.__Deblocks()
        self.__DCT()
        self.__Quantization()
        self.__ZigzagScan()
        self.__DPCM()
        self.__RLC()
        self.__EntropyCoding()

    # 颜色转换
    def __RGB2YCbCr(self):
        xform = np.array([[.299, .587, .114], [-.1687, -.331264, .5], [.5, -.418688, -.081312]])
        self.__YUVimg = self.__RGBimg.dot(xform.T)
        self.__YUVimg[:, :, [1, 2]] += 128
        self.__YUVimg = np.int32(self.__YUVimg)

    # 二次采样
    def __DoubleSampling(self):
        self.__YUVbands = [[], [], []]
        self.__YUVbands[0] = self.__YUVimg[..., 0]
        self.__YUVbands[1] = self.__YUVimg[::2, ::2, 1]
        self.__YUVbands[2] = self.__YUVimg[1::2, ::2, 2]

    # 补全规格化
    def __LengthSupplement(self, current):
        # supple 0 until the width and height of the image is eight's times
        while current.shape[0] % 8 != 0:
            current = np.insert(current, current.shape[0], values=0, axis=0)
        while current.shape[1] % 8 != 0:
            current = np.insert(current, current.shape[1], values=0, axis=1)
        return current

    # 分块
    def __Deblocks(self):
        self.__Blocks = [[], [], []]
        for t in range(3):
            current = self.__LengthSupplement(self.__YUVbands[t])
            # deblock the origin image to some 8*8 blocks
            height, width = current.shape
            for i in range(height // 8):
                for j in range(width // 8):
                    self.__Blocks[t].append(current[range(i * 8, i * 8 + 8)][:, range(j * 8, j * 8 + 8)])

    # 二维离散余弦变换
    def __DCT(self):
        self.__DCTed = [[], [], []]
        A = getDCTtable()
        for t in range(3):
            for current in self.__Blocks[t]:
                self.__DCTed[t].append(A.dot(current - 128).dot(np.transpose(A)))

    # 量化
    def __Quantization(self):
        self.__Quantizated = [[], [], []]
        # Y channel
        for t in range(3):
            for current in self.__DCTed[t]:
                temp = np.zeros((8, 8), dtype=int)
                for i in range(8):
                    for j in range(8):
                        temp[i, j] = int(round(current[i, j] / QuantizationTable[t][i][j]))
                self.__Quantizated[t].append(temp)

    # Z形扫描
    def __ZigzagScan(self):
        self.__Zigzaged = [[], [], []]
        for t in range(3):
            for current in self.__Quantizated[t]:
                temp = [0] * 64
                for i in range(8):
                    for j in range(8):
                        index = ZigzagTable[i][j]
                        temp[index] = current[i, j]
                self.__Zigzaged[t].append(temp)

    # 差分编码调制
    def __DPCM(self):
        self.__DPCMed = [[], [], []]
        for t in range(3):
            current = self.__Zigzaged[t]
            self.__DPCMed[t].append(current[0][0])
            for i in range(1, len(current)):
                DC = current[i][0] - current[i-1][0]
                self.__DPCMed[t].append(DC)

    # 游长编码
    def __RLC(self):
        self.__RLCed = [[], [], []]
        maxSize = 0
        for t in range(3):
            for block in self.__Zigzaged[t]:
                zeroNum = 0
                temp = []
                for i in range(1, 64):
                    if block[i] == 0:
                        zeroNum += 1
                        if zeroNum >= 15:
                            temp.append((15, 0))
                            zeroNum = 0
                    else:
                        temp.append((zeroNum, block[i]))
                        zeroNum = 0
                if zeroNum and len(temp) < 64:
                    temp.append((0, 0))
                self.__RLCed[t].append(temp)

    # 熵编码
    def __EntropyCoding(self):
        self.__DCcode = [[], [], []]
        self.__ACcode = [[], [], []]
        for t in range(3):
            # entropy coding on DC
            for current in self.__DPCMed[t]:
                amplitude = getAmplitude(current)
                size = len(amplitude)
                self.__DCcode[t].append((DC_HuffmanTable[t][size], amplitude))

            # entropy coding on AC
            for block in self.__RLCed[t]:
                temp = []
                for pair in block:
                    zeroNum = pair[0]
                    amplitude = getAmplitude(pair[1])
                    temp.append((AC_HuffmanTable[t][zeroNum][len(amplitude)], amplitude))
                self.__ACcode[t].append(temp)

    # 获得压缩数据
    def getCompressedData(self):
        return (self.__DCcode, self.__ACcode, self.__width, self.__height)
