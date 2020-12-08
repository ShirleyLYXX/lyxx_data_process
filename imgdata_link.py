import os
from shutil import copyfile
import numpy as np
import pandas as pd
import cv2
import font_util.commonly_util as cutil
from tqdm import tqdm
import re
import math
from util_rotate_img import rotate_img, rotate_points

def toarray(points):
    assert len(points)==8
    return np.array([[points[0], points[1]],[points[2], points[3]],[points[4], points[5]],[points[6], points[7]]], dtype=np.float32)



def dot_crop(img_path, result_txt, save_path):
    if not os.path.exists(save_path + "/images"):
        os.makedirs(save_path + "/images")
    if not os.path.exists(save_path + "/labelTxt"):
        os.makedirs(save_path + "/labelTxt")
    all_txt = open(os.path.join(save_path, 'labellink.txt'), 'w', encoding='utf-8')

    label_pd = cutil.label_tyre(result_txt)
    for file in tqdm(os.listdir(img_path)):
        img_ext = [".png",".jpg",".jpeg",".tif"]
        name = os.path.splitext(file)[0]
        if os.path.splitext(file)[1] not in img_ext:
            continue
        if name not in list(label_pd["img_name"]):
            print("Not inference result in picture:", name)
            continue

        img_result = label_pd[lambda x:x["img_name"]==name]
        img_result = pd.DataFrame(img_result.sort_values(by="height",ascending=True))
        img = cv2.imread(os.path.join(img_path, file), -1)
        dot_pattern = re.compile(r'[0-9]{2}[12][0-9](?![0-9])')
        #---------- return dot_cord, all_cord means all the cord except dot_cord -----------
        all_cord = []
        dot_cord = []
        all_cls = []
        for id, item in img_result.iterrows():
            match = dot_pattern.search(item["kind"])
            cord = item["cord"]
            if len(cord) == 4:
                cord = cutil.dots2ToRec8(cord)
            if match:
                dot_cord = cord
            
            all_cord.append(cord)
            all_cls.append(item["kind"])

        if dot_cord != [] and len(all_cord) > 1:
            order_cord = np.lexsort(np.array(all_cord)[:,::-1].T)
            for cord_ in range(len(all_cord)):
                if all_cord[cord_][0] == dot_cord[0]:
                    id_dot = cord_
                    break
            if np.where(id_dot==order_cord)[0][0] - 1 < 0 or np.where(id_dot==order_cord)[0][0] + 1 == len(order_cord):
                continue
            id_dis_left = order_cord[np.where(id_dot==order_cord)[0][0] - 1]
            id_dis_right = order_cord[np.where(id_dot==order_cord)[0][0] + 1]

            def area_rect(cord):
                return cv2.minAreaRect(toarray(cord))

            dot_angle = area_rect(all_cord[id_dot])[2]
            if dot_angle < -5 and dot_angle > -85:
                continue
            left_angle = area_rect(all_cord[id_dis_left])[2]
            right_angle = area_rect(all_cord[id_dis_right])[2]
        
            def get_delta(left_cord, right_cord):
                delta_x = right_cord[0] - left_cord[2]
                delta_y = abs(left_cord[3] - right_cord[1])
                if delta_x < 15 and delta_y < 10:
                    return delta_x, delta_y
                return

            def get_new_obj(cord_left, cord_right, angle, id_left, id_right):
                if get_delta(cord_left, cord_right) and (angle >= -5 or angle <= -90):
                    left_points = cv2.boxPoints(area_rect(cord_left))
                    right_points = cv2.boxPoints(area_rect(cord_right))

                    x_min = min(left_points[0][0],left_points[1][0])
                    x_max = max(right_points[2][0], right_points[3][0])
                    y_min = min(left_points[1][1],left_points[2][1],right_points[1][1],right_points[2][1])
                    y_max = max(left_points[0][1],left_points[3][1],right_points[0][1],right_points[3][1])

                    new_cord = [x_min, x_max, y_min, y_max]
                    new_label = all_cls[id_left] + '$' + all_cls[id_right]
                    return new_cord, new_label, id_left, id_right
                return None, None, id_left, id_right
            
            new_cord, new_label, left_id, right_id = get_new_obj(all_cord[id_dis_left], dot_cord, left_angle, id_dis_left, id_dot)
            if new_cord:
                img_ = img[int(new_cord[2]):int(new_cord[3]), int(new_cord[0]):int(new_cord[1])]
                subimgname = name + "_link_" + str(left_id) + '_' + str(right_id)
                cv2.imwrite(os.path.join(save_path + "/images", subimgname + ".png"), img_)
                all_txt.write(subimgname + '.png ' + new_label + '\n')

            new_cord, new_label, left_id, right_id = get_new_obj(dot_cord, all_cord[id_dis_right], right_angle, id_dot, id_dis_right)
            if new_cord:
                img_ = img[int(new_cord[2]):int(new_cord[3]), int(new_cord[0]):int(new_cord[1])]
                subimgname = name + "_link_" + str(left_id) + '_' + str(right_id)
                cv2.imwrite(os.path.join(save_path + "/images", subimgname + ".png"), img_)
                all_txt.write(subimgname + '.png ' + new_label + '\n')

    all_txt.close()


if __name__=="__main__":
    # choose_notDOTtest(img_path="./tyre_1123/images",eye_path="./craft_testrename",
    # ori_label="./tyre_1123/label.txt",save_path="./tyre_split",seed=1)
    # tyre_division(path="./tyre_split/tyre_choose/images",
    # ori_label="./tyre_split/tyre_choose/label.txt",save_path="./tyre_division1129",seed=1)
    workspace = "/home/workspace/lyxx_data_process/"
    dot_crop(img_path=workspace + "tyre_rename_modified_deleted_label",
    result_txt = workspace + "tyre_rename_modified_deleted_label/labelTxt",
    save_path = workspace + "tyre_rename_modified_deleted_label_dot_link2")
    # choose_56(img_path="/home/workspace/data/tyre_1123/images",
    # label_path="/home/workspace/data/tyre_1123/label.txt",
    # save_path="/home/workspace/data/tyre_num/")
    # choose_json(path="/home/workspace/data/tyre_num/",
    # json_path="/home/workspace/data/tyre_1123/json_path",
    # save_path="/home/workspace/data/tyre_num/json_path")
    # stick_font(img_path="/home/workspace/hesiqing/test_font/images",
    # save_path="/home/workspace/hesiqing/stat")
    # rename(path="./craft_test",save_path="./craft_testrename")