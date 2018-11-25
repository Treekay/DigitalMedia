import cv2

from utils import *

class Decompress(object):
    def __init__(self, data, resPath):
        # load compressed data
        self.__DCcode, self.__ACcode, self.__width, self.__height = data
        # do decompress
        blocks = [[], [], []]
        for t in range(3):
            dc, ac = self.__EntropyDecoding(self.__DCcode[t], self.__ACcode[t], t)
            zig = self.__IDCPM(dc)
            for i in range(len(zig)):
                zig[i] = self.__IRLC(ac[i], zig[i])
                qt = self.__IZigzagScan(zig[i])
                dct = self.__IQuantization(qt, t)
                blocks[t].append(self.__IDCT(dct))
        YUV = self.__IDeblocks(blocks)
        BGR = self.__YCbCr2BGR(YUV)
        self.__img = BGR[..., ::-1]
        self.getDecompressImg(resPath)

    # 熵解码器
    def __EntropyDecoding(self, DCcode, ACcode, t):
        dc = []
        ac = []
        for pair in DCcode:
            dc.append(amplitudeToValue(pair[1]))
        for block in ACcode:
            temp = []
            for pair in block:
                nextValue = amplitudeToValue(pair[1])
                zeroNum = getRunlength(t, len(pair[1]), pair[0])
                temp.append((zeroNum, nextValue))
            ac.append(temp)
        return (dc, ac)

    # 反DC系数
    def __IDCPM(self, current):
        zig = [[ current[0] ]]
        for i in range(1, len(current)):
            zig.append([zig[i - 1][0] + current[i]])
        return zig

    # 反AC系数
    def __IRLC(self, current, dc):
        zig = dc
        for pair in current:
            if pair[0] == 15 and pair[1] == 0:
                for i in range(15):
                    zig.append(0)
            elif pair[0] != 0 and pair[1] != 0:
                for i in range(pair[0]):
                    zig.append(0)
                zig.append(pair[1])
            elif pair[0] == 0 and pair[1] == 0:
                while len(zig) < 64:
                    zig.append(0)
            else:
                zig.append(pair[1])
        return zig
                
    # 反Zigzag
    def __IZigzagScan(self, current):
        qt = np.zeros((8, 8), dtype=int)
        for i in range(8):
            for j in range(8):
                qt[i, j] = current[ZigzagTable[i][j]]
        return qt

    # 反量化器
    def __IQuantization(self, current, t):
        dct = np.zeros((8, 8), dtype=int)
        for i in range(8):
            for j in range(8):
                dct[i, j] = current[i, j] * QuantizationTable[t][i][j]
        return dct

    # IDCT
    def __IDCT(self, current):
        return np.transpose(DCTtable).dot(current).dot(DCTtable) + 128

    # 逆分块补全, 二次采样
    def __IDeblocks(self, blocks):
        YUVimg = np.zeros((self.__height, self.__width, 3))
        ycols = np.int(np.ceil(self.__width / 8))
        uvcols = np.int(np.ceil(self.__width / 16))
        for i in range(self.__height):
            for j in range(self.__width):
                YUVimg[i, j, 0] = blocks[0][i // 8 * ycols + j // 8][i % 8][j % 8]
                YUVimg[i, j, 1] = blocks[1][i // 16 * uvcols + j // 16][i // 2 % 8][j // 2 % 8]
                YUVimg[i, j, 2] = blocks[2][i // 16 * uvcols + j // 16][i // 2 % 8][j // 2 % 8]
        return YUVimg

    # 颜色空间转换
    def __YCbCr2BGR(self, YUV):
        xform = np.array([[1, 0, 1.402], [1, -0.344136, -.714136], [1, 1.772, 0]])
        BGR = YUV.astype(np.float)
        BGR[:, :, [1, 2]] -= 128
        BGR = BGR.dot(xform.T)
        np.putmask(BGR, BGR > 255, 255)
        np.putmask(BGR, BGR < 0, 0)
        return np.uint8(BGR)

    # 得到压缩的图像
    def getDecompressImg(self, resPath):
        cv2.imshow('img', self.__img)
        cv2.imwrite(resPath, self.__img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
