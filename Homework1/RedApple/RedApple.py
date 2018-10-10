# -*- coding :utf-8 -*-
import copy

import cv2
import numpy as np
from PIL import Image
from progressbar import *

'''
    计算当前像素与颜色查找表每个颜色的最短欧式距离
    并找出距离最短的颜色作为该像素的代表颜色
    @param a: 矩阵1, 待处理的像素
    @param b: 矩阵2, 颜色查找表
'''
def findMinEdistancePos(a, b):
    return np.argmin(np.sqrt(np.sum(np.asarray(a - b) ** 2, axis = 1)))

'''
    @param str: 将要处理的图片文件路径
'''
def ImageProcess(str):
    # initial
    img = np.array(Image.open(str)) # 原图
    R, G, B = 0, 1, 2
    dim1, dim2, dim3 = img.shape
    img = np.reshape(img,(-1, 3))
    pixels = copy.deepcopy(img) # for process 

    
    # 按照中值区分算法对像素块进行排序划分成256个区域
    medianPos = len(pixels)
    for t in range(8):
        ltimes = len(pixels) // medianPos
        for i in range(ltimes):
            temp = pixels[i * medianPos : (i + 1) * medianPos]
            pixels[i * medianPos : (i + 1) * medianPos] = temp[np.lexsort(temp.T[t % 3,None])]
        medianPos = medianPos//2

    # 求出每个区域的平均RGB值作为代表颜色,共256个颜色组成颜色查找表
    regionLen = len(pixels)//256
    LUT = []
    for i in range(256):
        LUT.append(np.rint(np.mean(pixels[i * regionLen : (i + 1) * regionLen - 1],axis=0)).tolist())
    np.array(LUT)

    # 引进进度条
    widgets = ['Progress:',Percentage(), ' ', Bar('#'),' ', 
            Timer(), ' ', ETA(), ' ', FileTransferSpeed()]
    pbar = ProgressBar(widgets=widgets, maxval=len(img)).start()

    # 比较每个像素和LUT每个颜色的欧氏距离,将欧氏距离最短的颜色作为该像素的颜色
    for i in range(len(img)):
        # 更新进度条
        pbar.update(i)
        img[i] = LUT[findMinEdistancePos(a=img[i], b=LUT)]
    img = np.reshape(img,(dim1, dim2, dim3))
    pbar.finish()

    im = Image.fromarray(img)
    try:
        # 保存图片
        im.save('./img/hw2.jpg')
    except IOError:
        print("Error: file path error")
        cv2.imshow('AfterProcess', im)
    else:
        # 显示原图和处理后的图片进行比较
        cv2.imshow('OriginImage', cv2.imread('./img/redapple.jpg'))
        cv2.imshow('AfterProcess', cv2.imread('./img/hw2.jpg'))
        cv2.waitKey(0)
        ###press 'ESC' to exit

if __name__ == '__main__':
    ImageProcess(str='./img/redapple.jpg')