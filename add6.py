import os
import cv2
import shutil


def readtxt(data):
    items = []
    for item in data:
        items.append(item.strip())
    return items

enhance_num = 7
fe = open("enhance6/6_type3.txt", 'r', encoding='utf-8')
ftrain = open("tyre_1206/train/label.txt", 'r', encoding='utf-8')

enhance_ = fe.readlines()
enhance_ = readtxt(enhance_)
train_ = ftrain.readlines()
train_ = readtxt(train_)

fw = open("enhance6_type3_%d_label.txt" % enhance_num, 'w', encoding='utf-8')
train_enhance_ = []
for label in train_:
    img_ = label.split(' ')[0]
    label_ = label.split(' ')[1]
    if img_ in enhance_:
        train_enhance_.append(img_)
        img_name = img_.split('.')[0]
        for k in range(enhance_num):
            new_img_ = img_name +'_r%d.png' % k
            shutil.copy(os.path.join("tyre_rename_modified_deleted_label_cropped/images", img_name + '.png'), os.path.join("./enhance6_type3", new_img_))
            fw.write(new_img_ + ' ' + label_ + '\n')
print(len(train_enhance_))
print(len(enhance_))
#fw.close()
