import snap
import matplotlib.pyplot as plt
import os
import sys
import numpy as np

from TSS_utils import *

datasetPath = ""
if len(sys.argv) > 1:
    datasetPath = sys.argv[1]
else:
    sys.exit("Dataset path has to be specified")

#datasetPaths = ['./Datasets/Arxiv_GR-QC/CA-GrQc.txt', './Datasets/Arxiv_HEP-TH/CA-HepTh.txt']
threshold_const = [0,1,2,3,4,5,6,7,8,9,10]

#To check algorithm correctness we execute TSS algorithms (without considering probability on edges)
#  on some datasets experimented on paper, so we expect the same results 
print("TSS algorithm correctness (replicate paper experiments)")

datasetName = os.path.basename(os.path.normpath(datasetPath))
datasetName = os.path.splitext(datasetName)[0]

print("Dataset = ",datasetName)

target_set_size_values = []

for const in threshold_const:
    size_S = []
    G = snap.LoadEdgeList(snap.TUNGraph, datasetPath, 0, 1, '\t')
    node_threshold_mapping = threshold_setting(G, "constant", const=const)

    S = target_set_selection(G, node_threshold_mapping)
    target_set_size_values.append(len(S))

plt.scatter(threshold_const,target_set_size_values, marker="*", color="red")
plt.plot(threshold_const,target_set_size_values, color="red")
title = "My TSS with Dataset "+datasetName
plt.title(title)
plt.xlabel("Thresholds")
plt.ylabel("TSS Cardinality")
plt.xticks(np.arange(0, len(threshold_const)+1, 1))
file_name = "./graphics/algorithm_correctness/"+datasetName+"/"+datasetName+"_correctness.png"
plt.savefig(file_name)

