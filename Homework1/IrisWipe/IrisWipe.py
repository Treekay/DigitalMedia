# -*- coding :utf-8 -*-
import os
import math

import numpy as np
from PIL import Image
from progressbar import *

'''
    产生一个从图片1到图片2的虹膜擦拭切换动画gif图
    @param str1: the router of the image1
    @param str2: the router of the image2
'''
def ImageProcess(str1, str2):
    img1 = np.array(Image.open(str1))
    img2 = np.array(Image.open(str2))
    rows, cols, dims = img1.shape

    # 引进进度条
    widgets = ['Progress:',Percentage(), ' ',Bar('#'),' ', 
            Timer(), ' ', ETA(), ' ', FileTransferSpeed()]
    pbar = ProgressBar(widgets=widgets, maxval=300).start()

    '''
        半径从 0 逐渐增大, 圆内区域将图片1的像素值改为图片2的像素值
        对每一个半径大小修改后的图片, 保存到缓存列表
        完成整个变化过程后, 用缓存列表生成 gif 文件并显示
    '''
    r = 0
    frames = []
    while r <= 300:
        # 更新进度条
        pbar.update(r)
        for x in range(cols):
            for y in range(rows):
                if (pow(x - rows // 2 - 1,2) + 
                    pow(y - rows // 2 - 1,2) <= pow(r, 2)):
                    # change the circle region to lena
                    img1[x,y] = img2[x,y]
        r += 10
        # 将处理好的帧图片存进缓存队列
        frames.append(Image.fromarray(img1))

    try:
        # 生成并保存gif图
        frames[0].save('./img/hw1.gif', save_all=True, 
            append_images=frames[1:], duration=0.01, loop=0)
    except IOError:
        print("Error: file path error")
    else:
        # 显示gif图
        os.system(r"start ./img/hw1.gif")

    # process finish
    pbar.finish()

if __name__ == '__main__':
    ImageProcess(str1='./img/Nobel.jpg',
                str2='./img/lena.jpg')