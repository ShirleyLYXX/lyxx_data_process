# -*- coding:utf-8 -*-
import cv2
from math import *
import numpy as np
import time,math
import os
import re
from tqdm import tqdm
 
'''旋转图像并剪裁'''
def rotate(
        img,  # 图片
        pt1, pt2, pt3, pt4,
        newImagePath
):  
    rect = cv2.minAreaRect(np.float32(np.array([pt1,pt2,pt3,pt4])))
    box = np.array(cv2.boxPoints(rect), dtype=np.int32)
    angle = rect[2]
    pt1, pt2, pt3, pt4 = box
    # print (pt1,pt2,pt3,pt4)
    # withRect = math.sqrt((pt4[0] - pt1[0]) ** 2 + (pt4[1] - pt1[1]) ** 2)  # 矩形框的宽度
    # heightRect = math.sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) **2)
    # print (withRect,heightRect)
    # angle = acos((pt4[0] - pt1[0]) / withRect) * (180 / math.pi)  # 矩形框旋转角度
    # print (angle)
 
    if pt4[1] > pt1[1]:
        pass
        #print ("顺时针旋转")
    else:
        #print ("逆时针旋转")
        #angle = -angle
        if angle != 0.0:
            if angle < -45:
                angle += 90
    #print(angle)
    height = img.shape[0]  # 原始图像高度
    width = img.shape[1]   # 原始图像宽度
    rotateMat = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)  # 按angle角度旋转图像
    heightNew = int(width * fabs(sin(radians(angle))) + height * fabs(cos(radians(angle))))
    widthNew = int(height * fabs(sin(radians(angle))) + width * fabs(cos(radians(angle))))
 
    rotateMat[0, 2] += (widthNew - width) / 2
    rotateMat[1, 2] += (heightNew - height) / 2
    imgRotation = cv2.warpAffine(img, rotateMat, (widthNew, heightNew), borderValue=(255, 255, 255))
 
    # 旋转后图像的四点坐标
    [[pt1[0]], [pt1[1]]] = np.dot(rotateMat, np.array([[pt1[0]], [pt1[1]], [1]]))
    [[pt3[0]], [pt3[1]]] = np.dot(rotateMat, np.array([[pt3[0]], [pt3[1]], [1]]))
    [[pt2[0]], [pt2[1]]] = np.dot(rotateMat, np.array([[pt2[0]], [pt2[1]], [1]]))
    [[pt4[0]], [pt4[1]]] = np.dot(rotateMat, np.array([[pt4[0]], [pt4[1]], [1]]))
 
    # 处理反转的情况
    if pt2[1] > pt4[1]:
        pt2[1],pt4[1] = pt4[1],pt2[1]
    if pt1[0] > pt3[0]:
        pt1[0],pt3[0] = pt3[0],pt1[0]
 
    imgOut = imgRotation[int(pt2[1]):int(pt4[1]), int(pt1[0]):int(pt3[0])]
    cv2.imwrite(newImagePath, imgOut)  # 裁减得到的旋转矩形框
    return imgRotation  # rotated image
 
 
#　根据四点画原矩形
def drawRect(img,pt1,pt2,pt3,pt4,color,lineWidth):
    cv2.line(img, pt1, pt2, color, lineWidth)
    cv2.line(img, pt2, pt3, color, lineWidth)
    cv2.line(img, pt3, pt4, color, lineWidth)
    cv2.line(img, pt1, pt4, color, lineWidth)
 
#　读出文件中的坐标值
def ReadTxt(directory, imageName, last):
    img_suffix = ['.png', '.jpg', '.jpeg']
    flag = 0
    for suffix in img_suffix:
        if os.path.exists(os.path.join(directory, imageName + suffix)):
            imageName += suffix
            flag = 1
            break
    if flag==0:
        print("There is no %s" % imageName)
    #print(imageName)
    fileTxt = last  # txt文件名
    getTxt = open(fileTxt, 'r')  # 打开txt文件
    lines = getTxt.readlines()
    length = len(lines)
    for i in range(0, length):
        imgSrc = cv2.imread(os.path.join(directory, imageName))
        saveName = imageName.split('.')[0] + '_' + str(i) + '.png'
        items = lines[i].strip().split(',')
        if len(items) > 8:
            assert len(items) == 9
            if items[8] == '-1': # continue
                continue
            pt1 = [int(float(items[0])), int(float(items[1]))]
            pt4 = [int(float(items[2])), int(float(items[3]))]
            pt3 = [int(float(items[4])), int(float(items[5]))]
            pt2 = [int(float(items[6])), int(float(items[7]))]

            rotate(imgSrc, pt1, pt2, pt3, pt4, os.path.join('/home/workspace/lyxx_data_process/final_test_11tire_1207/crop_images', saveName))
            # cv2.imwrite('imgs_rotated/' + str(i) + '_' + saveName, rotated_img)
        else:
            #print(int(float(items[1])), int(float(items[3])), int(float(items[0])), int(float(items[2])))
            assert len(items) == 5
            if items[4] == '-1':
                continue
            items_ = list(float(items[i]) for i in range(len(items)-1))
            for j in range(len(items_)):
                if items_[j] < 0:
                    items_[j] = 0.0
                    print("0.0!!!%s" % saveName)
            items_ = [[items_[0], items_[1]], [items_[2], items_[3]]]
            x,y,w,h = cv2.boundingRect(np.float32(np.array(items_)))
            try:
                imgOut = imgSrc[y:y+h, x:x+w]
            except:
                print("Wrong!!!%s" % imageName)
                continue
            #imgOut = imgSrc[int(float(items[1])):int(float(items[3])),int(float(items[0])):int(float(items[2]))]
            cv2.imwrite(os.path.join('/home/workspace/lyxx_data_process/final_test_11tire_1207/crop_images', saveName), imgOut)
 
 #　读出文件中的坐标值
def ReadTxt_withlabel(directory, imageName, last):
    img_suffix = ['.png', '.jpg', '.jpeg']
    flag = 0
    for suffix in img_suffix:
        if os.path.exists(os.path.join(directory, imageName + suffix)):
            imageName += suffix
            flag = 1
            break
    if flag==0:
        print("There is no %s" % imageName)
    #print(imageName)
    fileTxt = last  # txt文件名
    getTxt = open(fileTxt, 'r')  # 打开txt文件
    lines = getTxt.readlines()
    length = len(lines)
    for i in range(0, length):
        imgSrc = cv2.imread(os.path.join(directory, imageName))
        saveName = imageName.split('.')[0] + '_' + str(i) + '.png'
        items = lines[i].strip().split(',')
        if len(items) > 8:
            assert len(items) == 9
            if items[8] == '-1': # continue
                continue
            pt1 = [int(float(items[0])), int(float(items[1]))]
            pt4 = [int(float(items[2])), int(float(items[3]))]
            pt3 = [int(float(items[4])), int(float(items[5]))]
            pt2 = [int(float(items[6])), int(float(items[7]))]

            rotate(imgSrc, pt1, pt2, pt3, pt4, os.path.join('/home/workspace/lyxx_data_process/final_test_11tire_1207/crop_images', saveName))
            # cv2.imwrite('imgs_rotated/' + str(i) + '_' + saveName, rotated_img)
        else:
            #print(int(float(items[1])), int(float(items[3])), int(float(items[0])), int(float(items[2])))
            assert len(items) == 5
            if items[4] == '-1':
                continue
            items_ = list(float(items[i]) for i in range(len(items)-1))
            for j in range(len(items_)):
                if items_[j] < 0:
                    items_[j] = 0.0
                    print("0.0!!!%s" % saveName)
            items_ = [[items_[0], items_[1]], [items_[2], items_[3]]]
            x,y,w,h = cv2.boundingRect(np.float32(np.array(items_)))
            try:
                imgOut = imgSrc[y:y+h, x:x+w]
            except:
                print("Wrong!!!%s" % imageName)
                continue
            #imgOut = imgSrc[int(float(items[1])):int(float(items[3])),int(float(items[0])):int(float(items[2]))]
            cv2.imwrite(os.path.join('/home/workspace/lyxx_data_process/final_test_11tire_1207/crop_images', saveName), imgOut)

if __name__=="__main__":
    directory = "/home/workspace/lyxx_data_process/final_test_11tire_1207/origin"
    #last = 'DOT%TR-BF-KM3#4__319.txt'
    #imageName = "DOT%TR-BF-KM3#4__319.jpeg"
    for file in tqdm(os.listdir(os.path.join(directory, 'labelTxt'))):
        last = os.path.join(directory, 'labelTxt', file)
        imageName = file.split('.')[0]
        ReadTxt(directory, imageName, last)
        
    #ReadTxt(directory, imageName, last)