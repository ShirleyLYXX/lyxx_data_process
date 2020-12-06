# -*- coding: utf-8 -*-
import cv2
import os
import json
import numpy as np
from mathutil import label_count, export_excel


# read json
def read_json(json_file):
    with open(json_file,'r',encoding='utf-8') as load_f:
        load_dict = json.load(load_f)
        return load_dict

# replace json
def replace_json(json_file, i):
    with open(json_file, "r+", encoding='utf-8') as jsonFile:
        data = json.load(jsonFile)
        
        # replace
        print(json_file, data["shapes"][i]['label'])
        del data["shapes"][i]    
    
        jsonFile.seek(0)  # rewind
        json.dump(data, jsonFile, indent=2, ensure_ascii=False)
        jsonFile.truncate()


def crop_and_save_img(img_o, area_, file_name):
    """
    img_o: np.array
    area: x_min, x_max, y_min, y_max
    """
    assert len(area_) == 4
    crop_img = img_o[area_[2]:area_[3],area_[0]:area_[1]]
    h = area_[3] - area_[2]
    w = area_[1] - area_[0]
    saveflag = '%d_%d' % (h, w)
    # cv2.imwrite(os.path.join(save_path, file_name + '_' + saveflag + '.png'), crop_img)
    return file_name + '_' + saveflag + '.png'


def process_coords(file):
    """
    return np.array(x_min,x_max,y_min,y_max)
    """
    dict_ = read_json(file)
    shapes = dict_['shapes']
    points = list([shape['points'] for shape in shapes])
    shapes_type = list([shape['shape_type'] for shape in shapes])
    label_ = list([shape['label'] for shape in shapes])

    # case
    area_array = []
    for idx in range(len(points)):
        points_ = points[idx]
        if shapes_type[idx] == 'rectangle':
            area_ = [int(points_[0][0]),int(points_[1][0]),int(points_[0][1]),int(points_[1][1])]
        else:
            # To do: 'polygan'
            x,y,w,h = cv2.boundingRect(np.float32(np.array(points_))) # left point
            area_ = [x, x+w, y, y+h]

        area_array.append(area_)
    return np.array(area_array), label_, len(label_)


if __name__ == '__main__':
    workspace = '/home/workspace/lyxx_data_process'
    data_path = 'part1_'
    # flag = 'M'
    # save_path = os.path.join(workspace, data_path + '_' + flag)
    # if not os.path.exists(save_path):
    #     os.mkdir(save_path)
    
    # read label2 img
    with open("label_2_1_del.txt", 'r') as f:
        lines = f.readlines()
        f.close()
    lines = [line.strip() for line in lines]
    
    # crop and save
    target_label = []
    filesname = []
    for file in os.listdir(os.path.join(workspace, data_path)):
        file_name = file.split('.')[0:-1]
        file_name = '.'.join(file_name)

        if file.endswith('.json'):
            area_array, label_, label_num = process_coords(os.path.join(workspace,data_path, file))
            for i in range(label_num):
                # filter
                # if label_[i] == '4X4':
                # if 'M' in label_[i]:
                    img_o = cv2.imread(os.path.join(workspace, data_path, file_name + '.jpeg'))
                    if img_o is None:
                        img_o = cv2.imread(os.path.join(workspace, data_path, file_name + '.jpg'))
                    if img_o is None:
                        img_o = cv2.imread(os.path.join(workspace, data_path, file_name + '.png'))
                    file_ = crop_and_save_img(img_o, area_array[i], file_name)
                    if file_ in lines:
                        #print(file)
                        replace_json(os.path.join(workspace, data_path, file), i)
                        break
                    #target_label.append(label_[i])
                    #filesname.append(file_name)
    
    # if target_label:
    #     with open('check_all_%s.txt' % flag, 'w+') as f:
    #     #with open('check_all_%s.txt' % flag, 'w+', encoding='utf-8') as f:
    #         for i in range(len(filesname)):
    #             f.write(filesname[i] + ' ' + target_label[i] + '\n')
    #         f.close()
    #     print(len(filesname))
        # export_data = np.array([filesname, target_label])
        # export_excel(export_data.T, os.path.join(save_path, 'label_%s.xlsx' % flag))
