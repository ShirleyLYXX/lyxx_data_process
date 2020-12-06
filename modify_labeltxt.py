

lines = []
with open('tyre_1123/label.txt', 'r') as f:
    lines = f.readlines()

for line in lines:
    line = line.split('/')[-1]
    names = line.split('.')[0]
    idx = names.split('_')[-1]
    imgName = '_'.join(names[0:-1])

    f = open(os.path.join("tyre_rename_modifed_deleted_label", imgName + '.json'), 'r')  
    