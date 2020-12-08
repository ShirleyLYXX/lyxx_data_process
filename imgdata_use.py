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

def rename(path,save_path):
    """
    rename tyre img file and json file
    """
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    for file in os.listdir(path):
        name=os.path.splitext(file)[0]
        ext=os.path.splitext(file)[1]
        ext_list=[".png",".jpg",".jpeg",".tif"]
        if ext not in ext_list:
            continue
        new_name=name.strip("_").replace(".jpeg","").replace(".jpg","").replace(".","_")
        copyfile(os.path.join(path,file),os.path.join(save_path,new_name+ext))
        copyfile(os.path.join(path,name+".json"),os.path.join(save_path,new_name+".json"))

def choose_notDOTtest(img_path,eye_path,ori_label,save_path,seed=1):
    test_save=os.path.join(save_path,"dan_test")
    choose_save=os.path.join(save_path,"tyre_choose")
    DOT_save=os.path.join(save_path,"DOT_remain")
    if not os.path.exists(test_save+"/images"):
        os.makedirs(test_save+"/images")
    if not os.path.exists(choose_save+"/images"):
        os.makedirs(choose_save+"/images")
    if not os.path.exists(DOT_save+"/images"):
        os.makedirs(DOT_save+"/images")
    try:
        label_pd=pd.read_pickle("./cache/tyre_1123.pkl")
    except:
        label_pd=cutil.label_del(ori_label)
        label_pd.to_pickle("./cache/tyre_1123.pkl")
    # print(label_pd)
    np.random.seed(seed)
    dot_pd=label_pd.loc[lambda x:x["label"]=="DOT"]
    dot_list=dot_pd["name"].values.tolist()
    DOT_choose=np.random.choice(dot_list,3744,replace=False)
    test_org=[os.path.splitext(i)[0] for i in os.listdir(eye_path)]
    # print(test_org)
    for file in tqdm(os.listdir(img_path)):
        name=os.path.splitext(file)[0]
        org_name="_".join(name.split("_")[0:-1])
        # print(org_name)
        file_dic=label_pd.loc[lambda x:x["name"]==name].iloc[0,]
        line=file_dic["line"]
        if org_name in test_org:
            with open(os.path.join(test_save,"label.txt"),"a") as tr:
                copyfile(os.path.join(img_path,file),os.path.join(test_save+"/images",file))
                tr.write(line)
        elif name not in DOT_choose:
            with open(os.path.join(choose_save,"label.txt"),"a") as chooser:
                copyfile(os.path.join(img_path,file),os.path.join(choose_save+"/images",file))
                chooser.write(line)
        else:
            with open(os.path.join(DOT_save,"label.txt"),"a") as dotr:
                copyfile(os.path.join(img_path,file),os.path.join(DOT_save+"/images",file))
                dotr.write(line)
def tyre_division(path,ori_label,save_path,seed=1):
    train_save=os.path.join(save_path,"train")
    valid_save=os.path.join(save_path,"valid")
    test_save=os.path.join(save_path,"test")
    if not os.path.exists(train_save+"/images"):
        os.makedirs(train_save+"/images")
    if not os.path.exists(valid_save+"/images"):
        os.makedirs(valid_save+"/images")
    if not os.path.exists(test_save+"/images"):
        os.makedirs(test_save+"/images")
    try:
        label_pd=pd.read_pickle("./cache/tyre_1123.pkl")
    except:
        label_pd=cutil.label_del(ori_label)
        label_pd.to_pickle("./cache/tyre_1123.pkl")
    np.random.seed(seed)
    img_list=os.listdir(path)
    test_list=np.random.choice(img_list,3449,replace=False)
    train_valid=list(set(img_list)-set(test_list))
    valid_list=np.random.choice(train_valid,5000,replace=False)
    # train_list=list(set(train_valid)-set(valid_list))
    for file in tqdm(img_list):
        name=os.path.splitext(file)[0]
        file_dic=label_pd.loc[lambda x:x["name"]==name].iloc[0,]
        line=file_dic["line"]
        
        label=file_dic["label"]
        if ")" in label or "(" in label or "_" in label:
            continue
        if file in test_list:
            with open(os.path.join(test_save,"label.txt"),"a") as testr:
                copyfile(os.path.join(path,file),os.path.join(test_save+"/images",file))
                testr.write(line)
        elif file in valid_list:
            with open(os.path.join(valid_save,"label.txt"),"a") as validr:
                copyfile(os.path.join(path,file),os.path.join(valid_save+"/images",file))
                validr.write(line)
        else:
            with open(os.path.join(train_save,"label.txt"),"a") as trainr:
                copyfile(os.path.join(path,file),os.path.join(train_save+"/images",file))
                trainr.write(line)

def dot_crop(img_path, result_txt, save_path):
    if not os.path.exists(save_path + "/images"):
        os.makedirs(save_path + "/images")
    if not os.path.exists(save_path + "/labelTxt"):
        os.makedirs(save_path + "/labelTxt")
    all_txt = open(os.path.join(save_path, 'label.txt'), 'w', encoding='utf-8')

    label_pd = cutil.label_tyre(result_txt)
    outlabelpath = save_path + "/labelTxt"
    for file in tqdm(os.listdir(img_path)):
        img_ext = [".png",".jpg",".jpeg",".tif"]
        name = os.path.splitext(file)[0]
        if os.path.splitext(file)[1] not in img_ext:
            continue
        # if name[0:3]=="DOT":
        #     continue
        if name not in list(label_pd["img_name"]):
            print("Not inference result in picture:", name)
            continue
        # big_img=cv2.imread(os.path.join(img_path,file),-1)
        # hh,ww=big_img.shape[0:2]
        # num=0

        img_result = label_pd[lambda x:x["img_name"]==name]
        img_result = pd.DataFrame(img_result.sort_values(by="height",ascending=True))
        img = cv2.imread(os.path.join(img_path, file), -1)
        # -------------the origin height, weight of whole image-------------
        (h, w) = img.shape[0:2]
        objects = [i[1] for i in img_result.iterrows()]

        dot_pattern = re.compile(r'[0-9]{2}[12][0-9](?![0-9])')
        #---------- return dot_cord, all_cord means all the cord except dot_cord -----------
        all_cord = []
        dot_cord = []
        id_dot = -1
        for id, item in img_result.iterrows():
            # if item["kind"].lower()!="DOT".lower():
            #     continue
            ratio = 0
            # np.random.choice(list(np.arange(0.5,0.9,(0.9-0.5)/10)))

            # -------------get the minimum bounding rectangle of the bbox-------------
            cord = item["cord"]
            if len(item["cord"])==4:
                cord = cutil.dots2ToRec8(item["cord"])
            #     cord = cutil.min_max_get(cord, ratio=ratio)
            # else:
            #     cord = cutil.min_max_get(item["cord"], ratio=ratio)
            
            match = dot_pattern.search(item["kind"])
            if match:
                #print(match.group())
                dot_cord = cord
                dot_label = item["kind"]
            
            all_cord.append(cord)

        if dot_cord != []:
            all_cord.remove(dot_cord)
            if all_cord == []:
                continue
            # ------------- Rotate img and points according to dot_cord and trans points to min_max ----
            assert len(dot_cord) == 8
            rotateMat, imgRotation = rotate_img(img, [dot_cord[0],dot_cord[1]],[dot_cord[2],dot_cord[3]],
                        [dot_cord[4],dot_cord[5]],[dot_cord[6],dot_cord[7]])
            dot_cord = rotate_points(rotateMat, [dot_cord[0],dot_cord[1]],[dot_cord[2],dot_cord[3]],[dot_cord[4],dot_cord[5]],[dot_cord[6],dot_cord[7]])
            dot_cord = cutil.min_max_get(dot_cord, ratio=ratio)
            dot_w = dot_cord[2] - dot_cord[0]
            dot_h = dot_cord[3] - dot_cord[1]
            for cord_ in range(len(all_cord)):
                all_cord[cord_] = rotate_points(rotateMat, [all_cord[cord_][0],all_cord[cord_][1]],[all_cord[cord_][2],all_cord[cord_][3]],
                        [all_cord[cord_][4],all_cord[cord_][5]],[all_cord[cord_][6],all_cord[cord_][7]])
                all_cord[cord_] = cutil.min_max_get(all_cord[cord_], ratio=ratio)
            
            # ------------ calculate the distance between other bboxes and dot bbox ------------
            dis_to_dot_left, dis_to_dot_right, dis_to_dot_up, dis_to_dot_down = [], [], [], []
            for idx in range(len(all_cord)):
                cur_cord = all_cord[idx]
                dis_to_dot_left.append(abs(dot_cord[0] - cur_cord[2]))
                dis_to_dot_right.append(abs(dot_cord[2] - cur_cord[0]))
                dis_to_dot_up.append(abs(dot_cord[1] - cur_cord[3]))
                dis_to_dot_down.append(abs(dot_cord[3] - cur_cord[1]))
            min_dis_left = min(dis_to_dot_left)
            min_dis_right = min(dis_to_dot_right)
            min_dis_up = min(dis_to_dot_up)
            min_dis_down = min(dis_to_dot_down)

            # ------------ the new bbox cord range, from left to right, up to down --------------
            (h_, w_) = imgRotation.shape[0:2]
            left = int(max(dot_cord[0]-min_dis_left, dot_cord[0]-math.ceil(dot_h/4)))
            right = int(min(dot_cord[2]+min_dis_right, dot_cord[2]+math.ceil(dot_h/4), w_))
            up = int(max(dot_cord[1]-min_dis_up, dot_cord[1]-math.ceil(dot_h/4)))
            down = int(min(dot_cord[3]+min_dis_down, dot_cord[3]+math.ceil(dot_h/4), h_))
            # img_roi=img[cord[1]:cord[3],cord[0]:min(cord[2]+(cord[2]-cord[0])*4,w)]
            # left, up, right, down=cord[0],cord[1],min(cord[2]+(cord[2]-cord[0])*4,w),cord[3]

            # ------------ increase the up boundry -----------
            img_roi_up = imgRotation[up:dot_cord[3], dot_cord[0]:dot_cord[2]]
            subimgname = name + "_up_" + str(dot_cord[0]) + '_' + str(up)
            cutil.savepatches(objects, subimgname, dot_cord[0], up, dot_cord[2], dot_cord[3], outlabelpath, rate=1)
            cv2.imwrite(os.path.join(save_path+"/images", subimgname + ".png"),img_roi_up)
            all_txt.write(subimgname + '.png ' + dot_label + '\n')
            # ------------ increase the down boundry -----------
            img_roi_down = imgRotation[dot_cord[1]:down, dot_cord[0]:dot_cord[2]]
            subimgname = name + "_down_" + str(dot_cord[0]) + '_' + str(dot_cord[1])
            cutil.savepatches(objects, subimgname, dot_cord[0], dot_cord[1], dot_cord[2], down, outlabelpath, rate=1)
            cv2.imwrite(os.path.join(save_path+"/images", subimgname + ".png"),img_roi_down)
            all_txt.write(subimgname + '.png ' + dot_label + '\n')
            # ------------ increase the left boundry -----------
            img_roi_left = imgRotation[dot_cord[1]:dot_cord[3], left:dot_cord[2]]
            subimgname = name + "_left_" + str(left) + '_' + str(dot_cord[1])
            cutil.savepatches(objects, subimgname, left, dot_cord[1], dot_cord[2], dot_cord[3], outlabelpath, rate=1)
            cv2.imwrite(os.path.join(save_path+"/images", subimgname + ".png"),img_roi_left)
            all_txt.write(subimgname + '.png ' + dot_label + '\n')
            # ------------ increase the right boundry -----------
            img_roi_right = imgRotation[dot_cord[1]:dot_cord[3], dot_cord[0]:right]
            subimgname = name + "_right_" + str(dot_cord[0]) + '_' + str(dot_cord[1])
            cutil.savepatches(objects, subimgname, dot_cord[0], dot_cord[1], right, dot_cord[3], outlabelpath, rate=1)
            cv2.imwrite(os.path.join(save_path+"/images", subimgname + ".png"),img_roi_right)
            all_txt.write(subimgname + '.png ' + dot_label + '\n')
            # ------------ increase all around boundry -----------
            img_roi_all = imgRotation[up:down, left:right]
            subimgname = name + "_around_" + str(left) + '_' + str(up)
            cutil.savepatches(objects, subimgname, left, up, right, down, outlabelpath, rate=1)
            cv2.imwrite(os.path.join(save_path+"/images", subimgname + ".png"),img_roi_all)
            all_txt.write(subimgname + '.png ' + dot_label + '\n')
    all_txt.close()

            # num+=1
def choose_56(img_path,label_path,save_path):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    label_pd=cutil.label_del(label_path)
    import re
    num=re.compile(r"[\d]+")
    for file in tqdm(os.listdir(img_path)):
        img_result=label_pd[lambda x:x["img_name"]==file].iloc[0,]
        label=img_result["label"]
        if len(num.findall(label))>0:
            copyfile(os.path.join(img_path,file),os.path.join(save_path,file))

def choose_json(path,json_path,save_path):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    name_list=[os.path.splitext(_)[0] for _ in os.listdir(path)]
    for file in os.listdir(json_path):
        name=os.path.splitext(file)[0]
        if name in name_list:
            copyfile(os.path.join(json_path,file),os.path.join(save_path,file))

def stick_font(img_path,save_path):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    font_pd=cutil.font_del(img_path)
    hh=font_pd["h"].sum()
    ww=font_pd["w"].max()*2
    max_h=font_pd["h"].max()
    font_img=np.zeros((hh,ww,3),np.uint8)
    font_img[:]=255
    h_start=0
    for file in os.listdir(img_path):
        name=os.path.splitext(file)[0]
        file_dic=font_pd.loc[lambda x:x["name"]==name].iloc[0,]
        h=file_dic["h"]
        w=file_dic["w"]
        img=cv2.imread(os.path.join(img_path,file),-1)
        # print(h,w,img.shape)
        cimg=cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
        font_img[h_start:h_start+h,0:w,:]=cimg
        text=file_dic["font"]
        point=(int(ww/2+1),int(h_start+h/2))
        cv2.putText(font_img, text, point, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1)
        h_start+=h
    cv2.imwrite(os.path.join(save_path,"font_style56.png"),font_img)
    print1=font_img[0:int(hh/3)+max_h,:,:]
    print2=font_img[int(hh/3):int(hh*2/3+max_h),:,:]
    print3=font_img[int(hh*2/3):hh,:,:]
    cv2.imwrite(os.path.join(save_path,"font_style56_print1.png"),print1)
    cv2.imwrite(os.path.join(save_path,"font_style56_print2.png"),print2)
    cv2.imwrite(os.path.join(save_path,"font_style56_print3.png"),print3)


if __name__=="__main__":
    # choose_notDOTtest(img_path="./tyre_1123/images",eye_path="./craft_testrename",
    # ori_label="./tyre_1123/label.txt",save_path="./tyre_split",seed=1)
    # tyre_division(path="./tyre_split/tyre_choose/images",
    # ori_label="./tyre_split/tyre_choose/label.txt",save_path="./tyre_division1129",seed=1)
    workspace = "/home/workspace/lyxx_data_process/"
    dot_crop(img_path=workspace + "tyre_rename_modified_deleted_label",
    result_txt = workspace + "tyre_rename_modified_deleted_label/labelTxt",
    # dot_crop(img_path=workspace + "tyre_debug",
    # result_txt = workspace + "tyre_debug/labelTxt",
    save_path = workspace + "tyre_rename_modified_deleted_label_dot_crop")
    # choose_56(img_path="/home/workspace/data/tyre_1123/images",
    # label_path="/home/workspace/data/tyre_1123/label.txt",
    # save_path="/home/workspace/data/tyre_num/")
    # choose_json(path="/home/workspace/data/tyre_num/",
    # json_path="/home/workspace/data/tyre_1123/json_path",
    # save_path="/home/workspace/data/tyre_num/json_path")
    # stick_font(img_path="/home/workspace/hesiqing/test_font/images",
    # save_path="/home/workspace/hesiqing/stat")
    # rename(path="./craft_test",save_path="./craft_testrename")