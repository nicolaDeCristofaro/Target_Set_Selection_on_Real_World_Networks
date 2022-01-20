import snap
import sys
import os
import matplotlib.pyplot as plt
import copy
import time

from TSS_utils import *

datasetPath = ""
if len(sys.argv) > 1:
    datasetPath = sys.argv[1]
else:
    sys.exit("Dataset path has to be specified")

#datasetPath = './Datasets/twitch/ENGB/musae_ENGB_edges.csv'
#datasetPath = './Datasets/Arxiv_GR-QC/CA-GrQc.txt'
#datasetPath = './Datasets/Arxiv_HEP-TH/CA-HepTh.txt'

datasetName = os.path.basename(os.path.normpath(datasetPath))
datasetName = os.path.splitext(datasetName)[0]

G = None
if datasetPath.endswith('.csv'):
    G = snap.LoadEdgeList(snap.TUNGraph, datasetPath, 0, 1, ',')
else:
    G = snap.LoadEdgeList(snap.TUNGraph, datasetPath, 0, 1, '\t')
print("\nOriginal graph info:")
print_graph_basic_info(G)
print_graph_deg_info(G)
print_graph_extra_info(G)

prob_functions = ["constant","constant","random","degree_based"]
prob_constants = [0.2,0.6]

thresholds_functions = ["constant","constant","degree_based", "degree_based"]
thresholds_const = [2,6]
thresholds_coeff = [(1,1),(2,7)]

i = 0
count = 0
c = 0
for prob_func in prob_functions:
    j = 0
    x = 0
    testsInfo = [dict() for x in range(4)]
    z = 0

    prob_const = 0
    if prob_func == "constant":
        prob_const = prob_constants[i]
        i += 1

    for thresholds_func in thresholds_functions:
        G = snap.LoadEdgeList(snap.TUNGraph, datasetPath, 0, 1, ',')
        if prob_func == "constant":
            edge_filtering(G, prob_func, const=prob_const)
        else:
            edge_filtering(G, prob_func)

        size_S = []
        print("\n***************************************************")
        print("\nSubgraph info:")
        print_graph_basic_info(G)

        if prob_func == "constant":
            if thresholds_func == "constant":
                print("\nTest {} (prob_func = {} {} - threshold_func = {} with const {})".format(count,prob_func,prob_const,thresholds_func,thresholds_const[x]))
                testsInfo[z]["threshold_func"] = thresholds_func + "(const=" + str(thresholds_const[x])+ ")"
            else:
                print("\nTest {} (prob_func = {} {} - threshold_func = {} with coeff ({},{}))".format(count,prob_func,prob_const,thresholds_func,thresholds_coeff[j][0],thresholds_coeff[j][1]))
                testsInfo[z]["threshold_func"] = thresholds_func + "(a=" + str(thresholds_coeff[j][0]) + ",b=" + str(thresholds_coeff[j][1]) + ")"
            
            testsInfo[z]["prob_func"] = prob_func + " " + str(prob_const)
        else:
            if thresholds_func == "constant":
                print("\nTest {} (prob_func = {} - threshold_func = {} with const {})".format(count,prob_func,thresholds_func,thresholds_const[x]))
                testsInfo[z]["threshold_func"] = thresholds_func + "(const=" + str(thresholds_const[x])+ ")"
            else:
                print("\nTest {} (prob_func = {} - threshold_func = {} with coeff ({},{}))".format(count,prob_func,thresholds_func,thresholds_coeff[j][0],thresholds_coeff[j][1]))
                testsInfo[z]["threshold_func"] = thresholds_func + "(a=" + str(thresholds_coeff[j][0]) + ",b=" + str(thresholds_coeff[j][1]) + ")"
            
            testsInfo[z]["prob_func"] = prob_func

        node_threshold_mapping_original = {}
        if thresholds_func == "constant":
            node_threshold_mapping_original = threshold_setting(G, thresholds_func, const=thresholds_const[x])
            if x == 1: x = 0
            else: x += 1
        else:
            node_threshold_mapping_original = threshold_setting(G, thresholds_func, a=thresholds_coeff[j][0],b=thresholds_coeff[j][1])
            if j == 1: j = 0
            else: j += 1

        print("\n*TSS execution...(10 iterations)")
        startTime = time.time()
        for k in range(0,10):
            node_threshold_mapping = copy.deepcopy(node_threshold_mapping_original)
            S = target_set_selection(G, node_threshold_mapping)
            size_S.append(len(S))
        
        avg_S_size = sum(size_S)/len(size_S)
        print(f"Execution Time: {round(time.time()-startTime, 2)} s")
        print("Average target set size for TEST {} = {}".format(count, math.ceil(avg_S_size)))
        print("\n***************************************************")
        print("\n")
        testsInfo[z]["avg_target_set_size"] = math.ceil(avg_S_size)
        z += 1
        count += 1

    #Generate and save the graphic
    threshold_func_values = list()
    avg_target_set_size_values = list()
    p_func = testsInfo[0]["prob_func"]
    for y in range(0,4):
        threshold_func_values.append(testsInfo[y]["threshold_func"])
        avg_target_set_size_values.append(testsInfo[y]["avg_target_set_size"])
    
    plt.figure(figsize=(20,10))

    plt.barh(threshold_func_values,avg_target_set_size_values, color=['red', 'green', 'blue', 'cyan'])
    title = "Avg target set size with "+ p_func + " probability func - varying threshold func"
    plt.title(title)
    plt.ylabel('Threshold function values')
    plt.xlabel('Avg target set size on 10 iterations')
    file_name = "./graphics/"+datasetName+"/avg_ts_size_"+str(c)+".png"
    plt.savefig(file_name)
    c += 1
