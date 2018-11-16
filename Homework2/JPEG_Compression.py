#JPEG compression algorithm
import cv2
import math
import numpy as np

def RGB2YCbCr(RGB):
    YUV = RGB
    width, height, dim = RGB.shape
    for x in range(width):
        for y in range(height):
            R = RGB[x, y, 2]
            G = RGB[x, y, 1]
            B = RGB[x, y, 0]
            YUV[x, y, 2] = 0.256789 * R + 0.504129 * G + 0.097906 * B + 16
            YUV[x, y, 1] = -0.148223 * R - 0.290992 * G + 0.439215 * B + 128
            YUV[x, y, 0] = 0.439215 * R - 0.367789 * G - 0.071426 * B + 128
    return YUV

def DoubleSampling(YUV):
    width, height, dim = YUV.shape
    Y = cv2.split(YUV)[2][range(width)][:, range(height)]
    U = cv2.split(YUV)[1][range(0, width, 2)][:, range(0, height, 2)]
    V = cv2.split(YUV)[0][range(1, width - 1, 2)][:, range(1, height - 1, 2)]
    return [Y, U, V]

def Deblock(mat):
    # 补0补到长宽都是8的倍数
    while mat.shape[0] % 8 != 0:
        mat = np.insert(mat, mat.shape[0], values=0, axis=0)
    while mat.shape[1] % 8 != 0:
        mat = np.insert(mat, mat.shape[1], values=0, axis=1)
    # 分为若干个8*8的子块
    width, height = mat.shape
    blocks = []
    for i in range(width // 8):
        for j in range(height // 8):
            blocks.append(mat[range(i, i + 8)][:, range(j, j + 8)])
    return blocks

def DCT(blocks):
    A = [] # DCT变换矩阵
    for i in range(8):
        for j in range(8):
            if i == 0:
                a = math.sqrt(1 / 8)
            else:
                a = math.sqrt(2 / 8)
            A.append(a * math.cos((j + 0.5) * math.pi * i / 8))
    A = np.array(A).reshape(8, 8).tolist()
    D = [] # DCT后的块
    for t in range(len(blocks)):
        D.append(A * blocks[t] * np.transpose(A))
    return D

def Quantization(Q, mode):
    if mode == 'Y':
        table = [[16, 11, 10, 16, 24, 40, 51, 61],
                 [12, 12, 14, 19, 26, 58, 60, 55],
                 [14, 13, 16, 24, 40, 57, 69, 56],
                 [14, 17, 22, 29, 51, 87, 80, 62],
                 [18, 22, 37, 56, 68, 109, 103, 77],
                 [24, 35, 55, 64, 81, 104, 113, 92],
                 [49, 64, 78, 87, 103, 121, 120, 101],
                 [72, 92, 95, 98, 112, 100, 103, 99]]
    else:
        table = [[17, 18, 24, 47, 99, 99, 99, 99],
                 [18, 21, 26, 66, 99, 99, 99, 99],
                 [24, 26, 56, 99, 99, 99, 99, 99],
                 [47, 66, 99, 99, 99, 99, 99, 99],
                 [99, 99, 99, 99, 99, 99, 99, 99],
                 [99, 99, 99, 99, 99, 99, 99, 99],
                 [99, 99, 99, 99, 99, 99, 99, 99],
                 [99, 99, 99, 99, 99, 99, 99, 99]]
    for t in range(len(Q)):
        for i in range(8):
            for j in range(8):
                Q[t][i, j] = int(round(Q[t][i, j] / table[i][j]))
    return Q

def Zigzag(Q):
    table = [[0, 1, 5, 6, 14, 15, 27, 28],
             [2, 4, 7, 13, 16, 26, 29, 42],
             [3, 8, 12, 17, 25, 30, 41, 43],
             [9, 11, 18, 24, 31, 40, 44, 53],
             [10, 19, 23, 32, 39, 45, 52, 54],
             [20, 22, 33, 38, 46, 51, 55, 60],
             [21, 34, 37, 47, 50, 56, 59, 61],
             [35, 36, 48, 49, 57, 58, 62, 63]]
    Z = []
    for t in range(len(Q)):
        temp = [0] * 64
        for i in range(8):
            for j in range(8):
                temp[table[i][j]] = Q[t][i, j]
        Z.append(temp)
    return Z

def DPCM(Z):
    Dp = []
    for t in range(len(Z)):
        temp = []
        value = Z[t][0]
        size = len(str(value))
        temp.append((size, value))
        for i in range(1, 64):
            value = Z[t][i] - Z[t][i-1]
            size = len(str(value))
            temp.append((size, value))
        Dp.append(temp)
    return Dp

def RLC(Z):
    pass
        


def Compression(srcPath, resPath):
    # 读取图像
    img = cv2.imread(srcPath)

    # 颜色空间转换: RGB -> YCbCr 
    YUV = RGB2YCbCr(img)

    # 二次采样 4:2:0
    Y, U, V = DoubleSampling(YUV)
    
    # 分块
    Yblocks = Deblock(Y)
    Ublocks = Deblock(U)
    Vblocks = Deblock(V)

    # 2D-DCT transform 离散余弦变换
    Y_DCT = DCT(Yblocks)
    U_DCT = DCT(Ublocks)
    V_DCT = DCT(Vblocks)

    # Quantization 量化
    Y_Q = Quantization(Y_DCT, 'Y')
    U_Q = Quantization(U_DCT, 'U')
    V_Q = Quantization(V_DCT, 'V')
    
    # Zigzag 扫描
    Y_Z = Zigzag(Y_Q)
    U_Z = Zigzag(U_Q)
    V_Z = Zigzag(V_Q)

    # DPCM 差分编码
    Y_DPCM = DPCM(Y_Z)
    U_DPCM = DPCM(U_Z)
    V_DPCM = DPCM(V_Z)

    # RLC 游长编码
    Y_RLC = RLC(Y_Z)
    U_RLC = RLC(U_Z)
    V_RLC = RLC(V_Z)

    # entropy coding 熵编码

    # 保存图像
    #img = Image.fromarray(img)
    #img.save(resPath)

if __name__ == "__main__":
    Compression('./src/cartoon.jpg', './res/cartoon.jpg')
    Compression('./src/reality.jpg', './res/reality.jpg') 
