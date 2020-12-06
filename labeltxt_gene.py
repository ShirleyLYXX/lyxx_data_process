# -*- coding:utf-8 -*-
import cv2
from math import *
import numpy as np
import time,math
import os
import re
from tqdm import tqdm
 
 
#　读出文件中的坐标值
def ReadTxt(directory, imageName, last):
    #print(imageName)
    fileTxt = last  # txt文件名
    getTxt = open(fileTxt, 'r', encoding='utf-8')  # 打开txt文件
    lines = getTxt.readlines()
    length = len(lines)
    labels = ''
    for i in range(0, length):
        saveName = imageName.split('.')[0] + '_' + str(i) + '.png'
        label_ = lines[i].strip().split(',')[-1]
        if label_ == "-1":
            continue
        if ' 1' in label_:
            label_ = label_.split(' ')[0]
        labels += saveName + ' ' + label_ + '\n'
    return labels
 
if __name__=="__main__":
    directory = "tyre_rename_modified_deleted_label"
    fw = open("labeltxt.txt", 'w', encoding='utf-8')
    for file in tqdm(os.listdir(os.path.join(directory, 'labelTxt'))):
        last = os.path.join(directory, 'labelTxt', file)
        imageName = file.split('.')[0]
        labels = ReadTxt(directory, imageName, last)
        fw.writelines(labels)
    fw.close()
