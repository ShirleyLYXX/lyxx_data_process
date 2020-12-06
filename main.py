import json
import os
import cv2
import numpy as np
import imgutil
from collections import defaultdict
import mathutil


# read json
def read_json(json_file):
    with open(json_file,'r') as load_f:
        load_dict = json.load(load_f)
        return load_dict


if __name__ == '__main__':
    worksapce = '/craft/tuhu_lyxx'
    data_path = '/craft/tuhu_lyxx/20201111_1'
    save_path = '/craft/tuhu_lyxx/target_data'
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    
    # collection and count
    label_all = []
    for file in os.listdir(data_path):
        if file.endswith('.json'):
            dict_ = read_json(os.path.join(data_path, file))
            shapes = dict_['shapes']
            label_ = list([shape['label'] for shape in shapes])
            label_all.extend(label_)
    mathutil.count(label_all, os.path.join(worksapce, 'label_count.xlsx'))
  