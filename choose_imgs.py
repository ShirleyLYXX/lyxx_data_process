import os
import shutil

with open("tyre_1206/test_all/label.txt", 'r', encoding='utf-8') as f:
    lines = f.readlines()
    print(len(lines))
    k = 0
    for line in lines:
        line = line.strip()
        img_ = line.split(' ')[0]
        if os.path.exists(os.path.join('tyre_rename_modified_deleted_label_cropped/images', img_)):
            k += 1
            shutil.copy(os.path.join("tyre_rename_modified_deleted_label_cropped/images", img_), os.path.join("./tyre_1206/test_all/images", img_))
print(k)
pass