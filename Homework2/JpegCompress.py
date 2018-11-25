#JpegCompress.py
import cv2

from utils import *

class Compress(object):
    def __init__(self, srcPath):
        # load image
        img = cv2.imread(srcPath)
        self.__height, self.__width, self.__dim = img.shape
        # do compress
        YUV = self.__RGB2YCbCr(img[:, :, :: -1])
        smp = self.__DoubleSampling(YUV)
        self.__DCcode = []
        self.__ACcode = []
        for t in range(3):
            blocks = self.__Deblocks(smp[t])
            zig = []
            ac = []
            for current in blocks:
                dct = self.__DCT(current)
                qt = self.__Quantization(dct, t)
                zigTemp = self.__ZigzagScan(qt)
                zig.append(zigTemp)
                ac.append(self.__RLC(zigTemp))
            dc = self.__DPCM(zig)
            temp = self.__EntropyCoding(dc, ac, t)
            self.__DCcode.append(temp[0])
            self.__ACcode.append(temp[1])

    # 颜色转换
    def __RGB2YCbCr(self, RGB):
        xform = np.array([[.299, .587, .114], [-.1687, -.331264, .5], [.5, -.418688, -.081312]])
        YUV = RGB.dot(xform.T)
        YUV[:, :, [1, 2]] += 128
        return np.int32(YUV)

    # 二次采样
    def __DoubleSampling(self, YUV):
        smp = [[], [], []]
        smp[0] = YUV[..., 0]
        smp[1] = YUV[::2, ::2, 1]
        smp[2] = YUV[1::2, ::2, 2]
        return smp

    # 补全规格化
    def __LengthSupplement(self, current):
        # supple 0 until the width and height of the image is eight's times
        while current.shape[0] % 8 != 0:
            current = np.insert(current, current.shape[0], values=0, axis=0)
        while current.shape[1] % 8 != 0:
            current = np.insert(current, current.shape[1], values=0, axis=1)
        return current

    # 分块
    def __Deblocks(self, smp):
        blocks = []
        current = self.__LengthSupplement(smp)
        # deblock the origin image to some 8*8 blocks
        height, width = current.shape
        for i in range(height // 8):
            for j in range(width // 8):
                blocks.append(current[range(i * 8, i * 8 + 8)][:, range(j * 8, j * 8 + 8)])
        return blocks

    # 二维离散余弦变换
    def __DCT(self, current):
        return DCTtable.dot(current - 128).dot(np.transpose(DCTtable))

    # 量化
    def __Quantization(self, current, t):
        qt = np.zeros((8, 8), dtype=int)
        for i in range(8):
            for j in range(8):
                qt[i, j] = int(round(current[i, j] / QuantizationTable[t][i][j]))
        return qt

    # Z形扫描
    def __ZigzagScan(self, current):
        zig = [0] * 64
        for i in range(8):
            for j in range(8):
                index = ZigzagTable[i][j]
                zig[index] = current[i, j]
        return zig

    # 差分编码调制
    def __DPCM(self, current):
        dc = [current[0][0]]
        for i in range(1, len(current)):
            DC = current[i][0] - current[i-1][0]
            dc.append(DC)
        return dc

    # 游长编码
    def __RLC(self, current):
        rc = []
        zeroNum = 0
        for i in range(1, 64):
            if current[i] == 0:
                zeroNum += 1
                if zeroNum >= 15:
                    rc.append((15, 0))
                    zeroNum = 0
            else:
                rc.append((zeroNum, current[i]))
                zeroNum = 0
        if zeroNum and len(rc) < 64:
            rc.append((0, 0))
        return rc

    # 熵编码
    def __EntropyCoding(self, dc, ac, t):
        DCcode = []
        ACcode = []
        # entropy coding on DC
        for current in dc:
            amplitude = getAmplitude(current)
            size = len(amplitude)
            DCcode.append((DC_HuffmanTable[t][size], amplitude))
        # entropy coding on AC
        for block in ac:
            temp = []
            for pair in block:
                zeroNum = pair[0]
                amplitude = getAmplitude(pair[1])
                temp.append((AC_HuffmanTable[t][zeroNum][len(amplitude)], amplitude))
            ACcode.append(temp)
        return (DCcode, ACcode)

    # 获得压缩数据
    def getCompressedData(self):
        return (self.__DCcode, self.__ACcode, self.__width, self.__height)