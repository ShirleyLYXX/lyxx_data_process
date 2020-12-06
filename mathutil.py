from collections import defaultdict
import os
import pandas as pd
import numpy as np


def export_excel(export, filename):
    pf = pd.DataFrame(export)
    pf.to_excel(filename)
    print(filename)


def label_count(label_all, filename):
    label_count = defaultdict(int)
    
    for label in label_all:
        if label not in label_count.keys():
            label_count[label] = 1
        else:
            label_count[label] += 1
    export_excel(label_count, filename)