import os
import json
from tqdm import tqdm

# json_path = "/home/workspace/lyxx_data_process/tyre_rename_modified_deleted_label/"
# txt_path = "/home/workspace/lyxx_data_process/tyre_rename_modified_deleted_label/labelTxt/"
json_path = "/home/workspace/lyxx_data_process/final_test_11tire_1207/"
txt_path = "/home/workspace/lyxx_data_process/final_test_11tire_1207/labelTxt/"
if not os.path.exists(txt_path):
    os.mkdir(txt_path)
jsons = os.listdir(json_path)
for jsonn in tqdm(jsons):
    if jsonn[-4:]!="json":
        continue
    txtn = jsonn[:-4] + "txt"
    labels = []
    with open(json_path + jsonn) as f1:
        s = json.load(f1)
    for shape in s["shapes"]:
        label = ""
        if len(shape["points"]) not in [4,2]:
            print ("points = %d : %s _%d" % (len(shape["points"]), jsonn, s["shapes"].index(shape)+1))
            # break
        # if shape["label"] == -1:
        #     print("kind -1:",jsonn)
        for p in shape["points"]:
            label += "%.1f,%.1f," % (float(int(p[0])), float(int(p[1])))
        label += str(shape["label"]) + '\n'
        labels.append(label)
    f2 = open(txt_path + txtn, 'w', encoding='utf-8')
    f2.writelines(labels)
    f2.close()

# img_path="E:/AI_game/subject4pre_game/test1"
# path=[i[0:-5] for i in os.listdir(json_path)]
# # print(path)
# with open("D:/no_label1.txt","w") as wr:
#     for file in sorted(os.listdir(img_path)):
#         if file[0:-4] not in path:
#             wr.write(file+"\n")

