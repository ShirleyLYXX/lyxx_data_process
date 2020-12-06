import os

with open('tyre_rename_delete.txt', 'r') as f:
    for line in f.readlines():
        line = line.strip()
        img_name = line.split('.')[0]
        os.remove(os.path.join('tyre1123_rotated_deleted/images', img_name + '.png'))
        print(line)
        