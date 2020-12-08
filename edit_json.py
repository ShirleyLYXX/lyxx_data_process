# -*- coding: utf-8 -*-
import cv2
import os
import json
import numpy as np
from mathutil import label_count, export_excel
import shutil
from tqdm import tqdm
import base64


# replace json
def edit_json(json_file, img_path):
    with open(json_file, "r+", encoding='utf-8') as jsonFile:
        data = json.load(jsonFile)
        
        # replace
        data["imagePath"] = img_path    
    
        jsonFile.seek(0)  # rewind
        json.dump(data, jsonFile, indent=2, ensure_ascii=False)
        jsonFile.truncate()


for file in tqdm(os.listdir("tyre_rename_modified_deleted_label")):
    imgexts = ['.png', '.jpg', '.jpeg']
    if file.endswith(".json"):
        img_name = file.split('.')[0]
        for ext in imgexts:
            if os.path.exists(os.path.join("tyre_rename_modified_deleted_label", img_name + ext)):
                edit_json(os.path.join("tyre_rename_modified_deleted_label", file), img_name + ext)
