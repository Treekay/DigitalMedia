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
        self.__IDoubleSampling()
        self.__YCbCr2RGB()

    # 熵解码器
    def __EntropyDecoding(self):
        self.__DPCMed = [[], [], []]
        self.__RLCed = [[], [], []]
        for t in range(3):
            for current in self.__DCcode[t]:
                self.__DPCMed[t].append(amplitudeToValue(current[1]))
            for current in self.__ACcode[t]:
                nextValue = amplitudeToValue(current[1])
                zeroNum = getRunlength(t, len(current[1]), current[0])
                self.__RLCed[t].append((zeroNum, nextValue))
    
    # 反DC系数
    def __IDCPM(self):
        self.__Zigzaged = [[], [], []]
        for t in range(3):
            temp = []
            current = self.__DPCMed[t]
            temp.append(current[0])
            self.__Zigzaged[t].append(temp)
            for i in range(1, len(self.__DPCMed[t])):
                temp = []
                temp.append(current[i - 1] + current[i])
                self.__Zigzaged[t].append(temp)

    # 反AC系数
    def __IRLC(self):
        for t in range(3):
            count = 0
            for pair in self.__RLCed[t]:
                ac = []
                if pair[0] == 0 and pair[1] == 0:
                    while len(self.__Zigzaged[t][count]) < 64:
                        self.__Zigzaged[t][count].append(0)
                    count += 1
                ac = ac + [0 for i in range(pair[0])] + [pair[1]]
                

    # 反Zigzag
    def __IZigzagScan(self):
        self.__Quantizated = [[], [], []]
        for t in range(3):
            for current in self.__Zigzaged[t]:
                print(len(current))
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
                temp = np.zeros((8, 8), dtype=int).tolist()
                for i in range(8):
                    for j in range(8):
                        temp[i][j] = current[i, j] * QuantizationTable[t][i][j]
                self.__DCTed[t].append(temp)

    # IDCT
    def __IDCT(self):
        self.__Blocks = [[], [], []]
        A = getDCTtable()
        for t in range(3):
            for current in self.__DCTed[t]:
                self.__Blocks[t].append(np.transpose(A) * current * A)

    # 逆分块补全, 二次采样
    def __IDeblocks(self):
        self.__YUVimg = []
        for i in range(self.__height):
            row = []
            for j in range(self.__width):
                Y = self.__Blocks[0][j // 8 * (i // 8 + 1)][i % 8][j % 8]
                U = self.__Blocks[1][j // 16 * (i // 16 + 1)][i // 2 % 8][j // 2 % 8]
                V = self.__Blocks[2][j // 16 * (i // 16 + 1)][i // 2 % 8][j // 2 % 8]
                row.append([V, U, Y])
            self.__YUVimg.append(row)

    # 颜色空间转换
    def __YCbCr2RGB(self):
        xform = np.array([[1, 0, 1.402], [1, -0.34414, -.71414], [1, 1.772, 0]])
        self.__img = self.__YUVimg.astype(np.float)
        self.__img[:, :, [1, 2]] -= 128
        self.__img = self.__img.dot(xform.T)
        np.putmask(self.__img, self.__img > 255, 255)
        np.putmask(self.__img, self.__img < 0, 0)
        self.__img = np.uint8(self.__img)

    # 得到压缩的图像
    def getDecompressImg(self):
        cv2.imshow(self.__img)
        cv2.waitKey(0)
        cv2.destoryAllWindows()
