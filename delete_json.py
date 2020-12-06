# -*- coding: utf-8 -*-
import cv2
import os
import json
import numpy as np
from mathutil import label_count, export_excel
import shutil
from tqdm import tqdm
import base64
# read json
def read_json(json_file):
    with open(json_file,'r',encoding='utf-8') as load_f:
        load_dict = json.load(load_f)
        return load_dict

# fw1 = open("tyre_rename_clean.txt", 'w')
# fw2 = open("tyre_rename_for_check.txt", 'w')
# for json_file in tqdm(os.listdir("./checked_1204")):
#     if json_file.endswith('.json'):
#         names = json_file.split('.')[0].split('_')
#         idx = int(names[-1])
#         imgName = '_'.join(names[0:-1])
#         dictJson = read_json(os.path.join("tyre_rename", imgName + '.json'))

#         dict_r = read_json(os.path.join("./checked_1204", json_file))
#         if len(dict_r['shapes'])==0:
#             dictJson['shapes'][idx]['label'] = -1
#             #print(imgName)
#         jj = open('tyre_rename_modified_deleted/' + imgName + '.json', 'w', encoding='utf-8')
#         json.dump(dictJson, jj, indent=2, ensure_ascii=False)
#         jj.close()
        #shutil.copy(os.path.join("./checked_1204", json_file), os.path.join("./checked_1204_clean", json_file))
            
# fw1.close()
# fw2.close()      
# 
# 
fw1 = open("tyre_rename_delete.txt", 'w')
for json_file in tqdm(os.listdir("./checked_1204")):
    if json_file.endswith('.json'):
        names = json_file.split('.')[0].split('_')
        idx = int(names[-1])
        imgName = '_'.join(names[0:-1])
        dictJson = read_json(os.path.join("tyre_rename", imgName + '.json'))

        dict_r = read_json(os.path.join("./checked_1204", json_file))
        if len(dict_r['shapes'])==0:
            # dictJson['shapes'][idx]['label'] = -1
            # #print(imgName)
            # for suffix in ['.jpg', '.jpeg', '.png']:
            #     if os.path.exists(os.path.join("tyre_rename", imgName + suffix)):
            #         img = cv2.imread(os.path.join("tyre_rename", imgName + suffix))
            #         imgext = suffix
            #         img_data = base64.b64encode(cv2.imencode(imgext, img)[1]).decode('utf-8')
            #         dictJson["imageData"] = img_data
            #         break
            # jj = open('tyre_rename_for_test/' + imgName + '.json', 'w')
            # json.dump(dictJson, jj, indent=2)
            # jj.close()
            fw1.write(json_file + '\n')
fw1.close()
        #shutil.copy(os.path.join("./checked_1204", json_file), os.path.join("./checked_1204_clean", json_file))    
