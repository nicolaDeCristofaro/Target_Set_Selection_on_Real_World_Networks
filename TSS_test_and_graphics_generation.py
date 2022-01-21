import snap
import sys
import os
import matplotlib.pyplot as plt
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

print("Dataset = ",datasetName)

print("\nOriginal Graph Info:")
print_graph_basic_info(G)
print_graph_deg_info(G)
print_graph_extra_info(G)

prob_functions = ["constant","constant","random","degree_based"]
prob_constants = [0.2,0.6]

thresholds_functions = ["constant","constant","degree_based", "degree_based"]
thresholds_constants = [2,6]
thresholds_coefficients = [(1,1),(2,7)]


count = 1
for i in range(0,len(prob_functions)):

    testsInfo = [dict() for x in range(4)] #To hold info about each test

    prob_func = prob_functions[i]
    prob_const = None
    if prob_func == "constant":
        prob_const = prob_constants[i]

    for j in range(0,len(thresholds_functions)):
        
        thresholds_func = thresholds_functions[j]
        threshold_const = None
        threshold_coeff_a = None
        threshold_coeff_b = None
        if thresholds_func == "constant":
            threshold_const = thresholds_constants[j]
        else:
            threshold_coeff_a =  thresholds_coefficients[j-2][0]
            threshold_coeff_b = thresholds_coefficients[j-2][1]

        #print info about the test
        print("\n***********************************************************************")
        print("Test {}".format(count))
        if prob_func == "constant":
            print("- Probability distribution function = {} with const = {}".format(prob_func,prob_const))
            testsInfo[j]["prob_func"] = prob_func + " " + str(prob_const)
        else:
            print("- Probability distribution function = {}".format(prob_func))
            testsInfo[j]["prob_func"] = prob_func
        
        if thresholds_func == "constant":
            print("- Threshold function = {} with const = {}".format(thresholds_func,threshold_const))
            testsInfo[j]["threshold_func"] = thresholds_func + "(const=" + str(threshold_const)+ ")"
        else:
            print("- Threshold function = {} with coeff (a= {},b={})".format(thresholds_func,threshold_coeff_a,threshold_coeff_b))
            testsInfo[j]["threshold_func"] = thresholds_func + "(a=" + str(threshold_coeff_a) + ",b=" + str(threshold_coeff_b) + ")"

        size_S = []
        for k in range(0,10): #10 iterations and then avg because of the probability on the edges
            print("#######################################################################")
            print("\nIteration ",k)

            #read the graph again (refresh original graph)
            G = None
            if datasetPath.endswith('.csv'):
                G = snap.LoadEdgeList(snap.TUNGraph, datasetPath, 0, 1, ',')
            else:
                G = snap.LoadEdgeList(snap.TUNGraph, datasetPath, 0, 1, '\t')

            print("\n*Edges pre-computation...")
            startTime = time.time()
            if prob_func == "constant":
                edge_filtering(G, prob_func, const=prob_const)
            else:
                edge_filtering(G, prob_func)
            print(f"Time taken: {round(time.time()-startTime, 2)} s")

            print("\nGraph Info after edges pre-computation:")
            print_graph_basic_info(G)

            print("\n*Treshold setting...")
            startTime = time.time()
            node_threshold_mapping = {}
            if thresholds_func == "constant":
                node_threshold_mapping = threshold_setting(G, thresholds_func, const=threshold_const)
            else:
                node_threshold_mapping = threshold_setting(G, thresholds_func, a=threshold_coeff_a,b=threshold_coeff_b)
            print(f"Time taken: {round(time.time()-startTime, 2)} s")

            print("\n*TSS execution...")
            startTime = time.time()
            S = target_set_selection(G, node_threshold_mapping)
            print("Target Set Size for Iteration {} -> {}".format(k,len(S)))
            print(f"Time taken: {round(time.time()-startTime, 2)} s")
            print("#######################################################################")
            size_S.append(len(S))
        
        avg_S_size = math.ceil(sum(size_S)/len(size_S))
        print("Average target set size for TEST {} = {}".format(count, avg_S_size))
        print("\n***************************************************")
        print("\n")
        testsInfo[j]["avg_target_set_size"] = avg_S_size
        count += 1

    #Generate and save the graphic
    threshold_func_values = list()
    avg_target_set_size_values = list()
    p_func = testsInfo[0]["prob_func"]
    for y in range(0,4):
        threshold_func_values.append(testsInfo[y]["threshold_func"])
        avg_target_set_size_values.append(testsInfo[y]["avg_target_set_size"])
    
    plt.figure(figsize=(20,10))

    plt.barh(threshold_func_values,avg_target_set_size_values, color=['#ffcce7', '#daf2dc', '#81b7d2', '#4d5198'])
    title = "Avg target set size with "+ p_func + " probability func - varying threshold func"
    plt.title(title)
    plt.ylabel('Threshold function values')
    plt.xlabel('Avg target set size on 10 iterations')
    file_name = "./graphics/algorithm_execution/"+datasetName+"/"+datasetName+"avg_ts_size_"+str(i)+".png"
    plt.savefig(file_name)
