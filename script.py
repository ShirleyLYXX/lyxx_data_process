#encoding: utf-8
import json
import os

mod_map = {
    # 'NEDVA': 'NEOVA',
    # 'RTS': 'ATS',
    # 'KINEGRY': 'KInERGy', # 先转为大写
    # 'RIDGESTONE': 'RIDGESTOnE',
    # 'M0': 'MO',
    # 'M0E': 'MOE',
    # 'VENTUS': 'veNtus',
    # 'ECOWING': 'eCOWInG',
    # 'WING': 'WInG',
    # 'CINTURATO': 'CintuRato',
    # 'ECOPIA': 'ECOPIa',
    # 'HANKOOK': 'HanKOOK'
}

def process_label(label):
    mod_ = []
    # if label.upper() in mod_map.keys():
    #     mod_ =  mod_map[label.upper()]
    if '×' in label:
        mod_ = label.replace('×', 'X')
    if '·' in label:
        mod_ = label.replace('·', '.')
    return mod_

# read label2 img
with open("label_2_1_del.txt", 'r') as f:
    lines = f.readlines()
    f.close()
label_2_json_list = []
for line in lines:
    list_ = line.split('.')[0:-1]
    json_ = '.'.join(list_[0:-1]) + '.2x.json'
    label_2_json_list.append(json_)

# modify json
data_path = '/home/workspace/lyxx_data_process/part1_'
for file in os.listdir(data_path):
    if file.endswith('.json'):
        with open(os.path.join(data_path, file), "r+", encoding='utf-8') as jsonFile:
            data = json.load(jsonFile)
            # del imageData
            # if 'imageData' in data.keys():
            #     del data['imageData']
            #     print(file)
            
            # replace
            shapes = data["shapes"]
            for i in range(len(shapes)):
                shape_label = shapes[i]['label']
                label_ = process_label(shape_label)
                if label_:
                    shapes[i]['label'] = label_
                    print(file, label_)
            data["shapes"] = shapes        
        
            # jsonFile.seek(0)  # rewind
            # json.dump(data, jsonFile, indent=2, ensure_ascii=False)
            # jsonFile.truncate()
