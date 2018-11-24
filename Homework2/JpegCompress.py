#JpegCompress.py
import cv2
import numpy as np

import utils

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
        # self.__EntropyCoding()

    '''
    @msg: convert image from RGB-ColorSpace to YUV-Colorspace
    '''
    def __RGB2YCbCr(self):
        xform = np.array([[.299, .587, .114], [-.1687, -.3313, .5], [.5, -.4187, -.0813]])
        self.__YUVimg = im.dot(xform.T)
        self.__YUVimg[:, :, [1, 2]] += 128
        self.__YUVimg = np.uint8(self.__YUVimg)

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
    @msg: Discrete Cosine Transform
    '''
    def __DCT(self):
        self.__DCTed = [[], [], []]
        A = getDCTtable()
        for t in range(3):
            for current in self.__Blocks[t]:
                self.__DCTed[t].append(A * current * np.transpose(A))

    '''
    @msg: quantizating the image blocks
    '''
    def __Quantization(self):
        self.__Quantizated = self.__DCTed
        # Y channel
        for current in self.__Quantizated[2]:
            for i in range(8):
                for j in range(8):
                    current[i, j] = int(round(current[i, j] / YquantizationTable[i][j]))
        # U, V channel
        for current in self.__Quantizated[1]:
            for i in range(8):
                for j in range(8):
                    current[i, j] = int(round(current[i, j] / UVquantizationTable[i][j]))
        for current in self.__Quantizated[0]:
            for i in range(8):
                for j in range(8):
                    current[i, j] = int(round(current[i, j] / UVquantizationTable[i][j]))

    '''
    @msg: zigzag scanning the 8*8-blocks to a 64-row
    '''
    def __ZigzagScan(self):
        self.__Zigzaged = [[], [], []]
        for t in range(3):
            for current in self.__Quantizated[t]:
                temp = [0] * 64
                for i in range(8):
                    for j in range(8):
                        temp[ZigzagTable[i][j]] = current[i, j]
                self.__Zigzaged[t].append(temp)


    '''
    @msg: Differential Pulse Code Modulation
    '''
    def __DPCM(self):
        self.__DPCMed = [[], [], []]
        for t in range(3):
            for current in self.__Zigzaged[t]:
                DC = current[0]
                self.__DPCMed[t].append(DC)
                for i in range(1, 64):
                    DC = current[i] - current[i-1]
                    self.__DPCMed[t].append(DC)

    '''
    @msg: Run Length Coding
    '''
    def __RLC(self):
        self.__RLCed = [[], [], []]
        maxSize = 0
        for t in range(3):
            for current in self.__Zigzaged[t]:
                zeroNum = 0
                for i in range(1, 63):
                    if current[i] == 0:
                        zeroNum += 1
                    else:
                        self.__RLCed[t].append((zeroNum , current[i+1]))
                        zeroNum = 0
                self.__RLCed[t].append((0, 0)) # EOB

    def getAmplitude(num):
        if num > 0:
            return bin(num).replace('0b', '')
        else:
            return bin(~num).replace('0b', '')

    '''
    @msg: Entropy Coding using Huffman coding and VLI coding
    '''
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
            for current in self.__RLCed[t]:
                zeroNum = current[0]
                nextValue = current[1]
                amplitude = getAmplitude(nextValue)
                while zeroNum > 15:
                    self.__ACcode[t].append((AC_HuffmanTable[t][15][0], ''))
                    zeroNum -= 15
                self.__ACcode[t].append((AC_HuffmanTable[t][zeroNum][len(str(nextValue))], amplitude))

    '''
    @msg: return the compressed image data
    '''
    def getCompressedData(self):
        return (self.__DCcode, self.__ACcode)
