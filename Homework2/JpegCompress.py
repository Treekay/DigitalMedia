#JpegCompress.py
import cv2
import math
import numpy as np

class Compress(object):
    def __init__(self, srcPath):
        # load image
        self.__RGBimg = cv2.imread(srcPath)
        self.__width, self.__height, self.__dim = self.__RGBimg.shape
        # do compress
        self.__RGB2YCbCr()
        self.__DoubleSampling()
        self.__Deblocks()
        self.__DCT()
        self.__Quantization()
        self.__ZigzagScan()
        self.__DPCM()
        self.__RLC()
        self.__HuffmanCoding()

    '''
    @msg: convert image from RGB-ColorSpace to YUV-Colorspace
    '''
    def __RGB2YCbCr(self):
        self.__YUVimg = self.__RGBimg
        for x in range(self.__width):
            for y in range(self.__height):
                R = self.__RGBimg[x, y, 2] 
                G = self.__RGBimg[x, y, 1]
                B = self.__RGBimg[x, y, 0]
                self.__YUVimg[x, y, 2] = 0.256789 * R + 0.504129 * G + 0.097906 * B + 16
                self.__YUVimg[x, y, 1] = -0.148223 * R - 0.290992 * G + 0.439215 * B + 128
                self.__YUVimg[x, y, 0] = 0.439215 * R - 0.367789 * G - 0.071426 * B + 128

    '''
    @msg: double sampling the YUV-ColorSpace image
    '''
    def __DoubleSampling(self):
        self.__YUVbands = [[], [], []]
        self.__YUVbands[2] = cv2.split(self.__YUVimg)[2][range(self.__width)][:, range(self.__height)]
        self.__YUVbands[1] = cv2.split(self.__YUVimg)[1][range(0, self.__width, 2)][:, range(0, self.__height, 2)]
        self.__YUVbands[0] = cv2.split(self.__YUVimg)[0][range(1, self.__width - 1, 2)][:, range(1, self.__height - 1, 2)]

    '''
    @msg: supple the width and height of each channel of the image to eight's times
    @param {list[[]]} currrent: the origin list
    @return: a eight's times list
    '''
    def __LengthSupplement(self, current):
        # supple 0 until the width and height of the image is eight's times
        while current.shape[0] % 8 != 0:
            current = np.insert(current, current.shape[0], values=0, axis=0)
        while current.shape[1] % 8 != 0:
            current = np.insert(current, current.shape[1], values=0, axis=1)
        return current
              
    '''
    @msg: deblock the origin image to some 8*8 blocks
    '''
    def __Deblocks(self):
        self.__Blocks = [[], [], []]
        for t in range(3):
            current = self.__LengthSupplement(self.__YUVbands[t])
            # deblock the origin image to some 8*8 blocks
            width, height = current.shape
            for i in range(width // 8):
                for j in range(height // 8):
                    self.__Blocks[t].append(current[range(i, i + 8)][:, range(j, j + 8)])

    '''
    @msg: generate a DCT transform matrix
    @return: a DCT transform matrix
    '''
    def __DCTtableGenerate(self):
        A = []  # DCT transform matrix
        for i in range(8):
            for j in range(8):
                if i == 0:
                    a = math.sqrt(1 / 8)
                else:
                    a = math.sqrt(2 / 8)
                A.append(a * math.cos((j + 0.5) * math.pi * i / 8))
        A = np.array(A).reshape(8, 8).tolist()
        return A

    '''
    @msg: Discrete Cosine Transform
    '''
    def __DCT(self):
        self.__DCTed = [[], [], []]
        A = self.__DCTtableGenerate()
        for t in range(3):
            for current in self.__Blocks[t]:
                self.__DCTed[t].append(A * current * np.transpose(A))

    '''
    @msg: quantizating the image blocks
    '''
    def __Quantization(self):
        self.__Quantizated = self.__DCTed
        # Y channel
        table = [[16, 11, 10, 16, 24, 40, 51, 61],
                [12, 12, 14, 19, 26, 58, 60, 55],
                [14, 13, 16, 24, 40, 57, 69, 56],
                [14, 17, 22, 29, 51, 87, 80, 62],
                [18, 22, 37, 56, 68, 109, 103, 77],
                [24, 35, 55, 64, 81, 104, 113, 92],
                [49, 64, 78, 87, 103, 121, 120, 101],
                [72, 92, 95, 98, 112, 100, 103, 99]]
        for current in self.__Quantizated[0]:
            for i in range(8):
                for j in range(8):
                    current[i, j] = int(round(current[i, j] / table[i][j]))
        # U, V channel
        table = [[17, 18, 24, 47, 99, 99, 99, 99],
                [18, 21, 26, 66, 99, 99, 99, 99],
                [24, 26, 56, 99, 99, 99, 99, 99],
                [47, 66, 99, 99, 99, 99, 99, 99],
                [99, 99, 99, 99, 99, 99, 99, 99],
                [99, 99, 99, 99, 99, 99, 99, 99],
                [99, 99, 99, 99, 99, 99, 99, 99],
                [99, 99, 99, 99, 99, 99, 99, 99]]
        for current in self.__Quantizated[1]:
            for i in range(8):
                for j in range(8):
                    current[i, j] = int(round(current[i, j] / table[i][j]))
        for current in self.__Quantizated[2]:
            for i in range(8):
                for j in range(8):
                    current[i, j] = int(round(current[i, j] / table[i][j]))

    '''
    @msg: zigzag scanning the 8*8-blocks to a 64-row
    '''
    def __ZigzagScan(self):
        self.__Zigzaged = [[], [], []]
        table = [[0, 1, 5, 6, 14, 15, 27, 28],
                [2, 4, 7, 13, 16, 26, 29, 42],
                [3, 8, 12, 17, 25, 30, 41, 43],
                [9, 11, 18, 24, 31, 40, 44, 53],
                [10, 19, 23, 32, 39, 45, 52, 54],
                [20, 22, 33, 38, 46, 51, 55, 60],
                [21, 34, 37, 47, 50, 56, 59, 61],
                [35, 36, 48, 49, 57, 58, 62, 63]]
        for t in range(3):
            for current in self.__Quantizated[t]:
                temp = [0] * 64
                for i in range(8):
                    for j in range(8):
                        temp[table[i][j]] = current[i, j]
                self.__Zigzaged[t].append(temp)

    '''
    @msg: Differential Pulse Code Modulation
    '''
    def __DPCM(self):
        self.__DPCMed = [[], [], []]
        for t in range(3):
            for current in self.__Zigzaged[t]:
                temp = []
                value = current[0]
                size = len(str(value))
                temp.append((size, value))
                for i in range(1, 64):
                    value = current[i] - current[i-1]
                    size = len(str(value))
                    temp.append((size, value))
                self.__DPCMed[t].append(temp)

    '''
    @msg: Run Length Coding
    '''
    def __RLC(self):
        self.__RLCed = [[], [], []]
        for t in range(3):
            current = self.__Zigzaged[t]
            zeroNum = (1 if current == 0 else 0)
            for i in range(1, len(current)):
                nextValue = current[i]
                if nextValue == 0:
                    zeroNum += 1
                    if zeroNum >= 16:
                        self.__RLCed[t].append((15, 0))
                        zeroNum = 1
                else:
                    # AC.append((zeroNum, nextValue))
                    self.__RLCed[t].append(((zeroNum / len(str(nextValue))), nextValue))
            self.__RLCed[t].append((0, 0)) # EOB

    '''
    @msg: Entropy Coding using Huffman coding
    '''
    def __HuffmanCoding(self):
        # Y-DC
        Y_DC_Huffman_Table = [000, 010, 011, 100, 101, 110, 1110, 11110, 111110, 1111110, 11111110, 111111110]
        Y_DC_VLI_Table = []
        # UV -DC
        UV_DC_Huffman_Table = []
        UV_DC_VLI_Table = []
        # Y-AC
        Y_AC_Huffman_Table = []
        Y_AC_VLI_Table = []
        # UV - AC
        UV_AC_Huffman_Table = []
        UV_AC_VLI_Table = []

    '''
    @msg: return the compressed image data
    '''
    def getCompressedData(self):
        pass