#JpegCompress.py
import cv2

from utils import *

class Decompress(object):
    def __init__(self, data, resPath):
        # load compressed data
        self.__DCcode, self.__ACcode, self.__width, self.__height = data
        # do decompress
        self.__EntropyDecoding()
        self.__IDCPM()
        self.__IRLC()
        self.__IZigzagScan()
        self.__IQuantization()
        self.__IDCT()
        self.__IDeblocks()
        self.__YCbCr2RGB()

    # 熵解码器
    def __EntropyDecoding(self):
        self.__DPCMed = [[], [], []]
        self.__RLCed = [[], [], []]
        for t in range(3):
            for pair in self.__DCcode[t]:
                self.__DPCMed[t].append(amplitudeToValue(pair[1]))
            for block in self.__ACcode[t]:
                temp = []
                for pair in block:
                    nextValue = amplitudeToValue(pair[1])
                    zeroNum = getRunlength(t, len(pair[1]), pair[0])
                    temp.append((zeroNum, nextValue))
                self.__RLCed[t].append(temp)
    
    # 反DC系数
    def __IDCPM(self):
        self.__Zigzaged = [[], [], []]
        for t in range(3):
            current = self.__DPCMed[t]
            self.__Zigzaged[t].append([current[0]])
            for i in range(1, len(current)):
                self.__Zigzaged[t].append([self.__Zigzaged[t][i - 1][0] + current[i]])

    # 反AC系数
    def __IRLC(self):
        for t in range(3):
            count = 0
            for block in self.__RLCed[t]:
                ac = self.__Zigzaged[t][count]
                for pair in block:
                    if pair[0] == 15 and pair[1] == 0:
                        for i in range(15):
                            ac.append(0)
                    elif pair[0] != 0 and pair[1] != 0:
                        for i in range(pair[0]):
                            ac.append(0)
                        ac.append(pair[1])
                    elif pair[0] == 0 and pair[1] == 0:
                        while len(ac) < 64:
                            ac.append(0)
                    else:
                        ac.append(pair[1])
                self.__Zigzaged[t][count] = ac
                count += 1
                
    # 反Zigzag
    def __IZigzagScan(self):
        self.__Quantizated = [[], [], []]
        for t in range(3):
            for current in self.__Zigzaged[t]:
                temp = np.zeros((8, 8), dtype=int).tolist()
                for i in range(8):
                    for j in range(8):
                        temp[i][j] = current[ZigzagTable[i][j]]
                self.__Quantizated[t].append(temp)

    # 反量化器
    def __IQuantization(self):
        self.__DCTed = [[], [], []]
        for t in range(3):
            for current in self.__Quantizated[t]:
                temp = np.zeros((8, 8), dtype=int)
                for i in range(8):
                    for j in range(8):
                        temp[i, j] = current[i][j] * QuantizationTable[t][i][j]
                self.__DCTed[t].append(temp)

    # IDCT
    def __IDCT(self):
        self.__Blocks = [[], [], []]
        A = getDCTtable()
        for t in range(3):
            for current in self.__DCTed[t]:
                self.__Blocks[t].append(np.transpose(A).dot(current).dot(A) + 128)

    # 逆分块补全, 二次采样
    def __IDeblocks(self):
        self.__YUVimg = np.zeros((self.__height, self.__width, 3))
        ycols = np.int(np.ceil(self.__width / 8))
        uvcols = np.int(np.ceil(self.__width / 16))
        for i in range(self.__height):
            for j in range(self.__width):
                self.__YUVimg[i, j, 0] = self.__Blocks[0][i // 8 * ycols + j // 8][i % 8][j % 8]
                self.__YUVimg[i, j, 1] = self.__Blocks[1][i // 16 * uvcols + j // 16][i // 2 % 8][j // 2 % 8]
                self.__YUVimg[i, j, 2] = self.__Blocks[2][i // 16 * uvcols + j // 16][i // 2 % 8][j // 2 % 8]

    # 颜色空间转换
    def __YCbCr2RGB(self):
        xform = np.array([[1, 0, 1.402], [1, -0.344136, -.714136], [1, 1.772, 0]])
        self.__img = self.__YUVimg.astype(np.float)
        self.__img[:, :, [1, 2]] -= 128
        self.__img = self.__img.dot(xform.T)
        np.putmask(self.__img, self.__img > 255, 255)
        np.putmask(self.__img, self.__img < 0, 0)
        self.__img = np.uint8(self.__img)

    # 得到压缩的图像
    def getDecompressImg(self):
        cv2.imshow('img', self.__img[..., ::-1])
        cv2.waitKey(0)
