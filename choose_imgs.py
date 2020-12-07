import os
import shutil

with open("tyre_1206/valid/label.txt", 'r', encoding='utf-8') as f:
    for line in f.readlines():
        line = line.strip()
        img_ = line.split(' ')[0]
        if os.path.exists(os.path.join('tyre_rename_modified_deleted_label_cropped/images', img_)):
            shutil.copy(os.path.join("tyre_rename_modified_deleted_label_cropped/images", img_), os.path.join("./tyre_1206/train/images", img_))
pass