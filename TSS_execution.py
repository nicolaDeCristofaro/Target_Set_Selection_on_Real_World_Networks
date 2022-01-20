import snap
import sys
import time
import os

from TSS_utils import *

#DEFAULT args
datasetPath = './Datasets/twitch/ENGB/musae_ENGB_edges.csv'
#datasetPath = './Datasets/Arxiv_GR-QC/CA-GrQc.txt'
#datasetPath = './Datasets/Arxiv_HEP-TH/CA-HepTh.txt'

prob_function = "degree_based"
prob_const = ""
treshold_function = "degree_based"
tresholds_const = ""
tresholds_coeff = [1,2]

if len(sys.argv) > 3:
    print("\nTSS Execution")
    datasetPath = sys.argv[1]
    prob_function = sys.argv[2]
    if prob_function == "constant":
        prob_const = float(sys.argv[3])
        treshold_function = sys.argv[4]
        if treshold_function == "constant":
            tresholds_const = int(sys.argv[5])
            print("\t =(prob_func = {} {} \n \t   treshold_func = {} with const {})".format(prob_function,prob_const,treshold_function,tresholds_const))
        else:
            tresholds_coeff[0] = int(sys.argv[5])
            tresholds_coeff[1] = int(sys.argv[6])
            print("\t =(prob_func = {} {} \n \t   treshold_func = {} with coeff ({},{}))".format(prob_function,prob_const,treshold_function,tresholds_coeff[0],tresholds_coeff[1]))
    else:
        treshold_function = sys.argv[3]
        if treshold_function == "constant":
            tresholds_const = int(sys.argv[4])
            print("\t =(prob_func = {} \n \t   treshold_func = {} with const {})".format(prob_function,treshold_function,tresholds_const))
        else:
            tresholds_coeff[0] = int(sys.argv[4])
            tresholds_coeff[1] = int(sys.argv[5])
            print("\t =(prob_func = {} \n \t   treshold_func = {} with coeff ({},{}))".format(prob_function,treshold_function,tresholds_coeff[0],tresholds_coeff[1]))
else:
    #NO params or incorrect number: DEFAULT EXECUTION
    print("TSS Execution - No params or incorrect number of params, so the DEFAULT values will be considered")
    print("\t =(prob_func = {} \n \t  treshold_func = {} with coeff ({},{}))".format(prob_function,treshold_function,tresholds_coeff[0],tresholds_coeff[1]))

# Load graph
G = None
if datasetPath.endswith('.csv'):
    G = snap.LoadEdgeList(snap.TUNGraph, datasetPath, 0, 1, ',')
else:
    G = snap.LoadEdgeList(snap.TUNGraph, datasetPath, 0, 1, '\t')

datasetName = os.path.basename(os.path.normpath(datasetPath))
datasetName = os.path.splitext(datasetName)[0]

print("Dataset = ",datasetName)

print("\nOriginal Graph Info:")
print_graph_basic_info(G)
print_graph_deg_info(G)
print_graph_extra_info(G)

size_S = []
startTotalTime = time.time()
for i in range(0,10): #10 iterations of TSS operations
    if i > 0:
        #read the graph again (refresh original graph)
        G = None
        if datasetPath.endswith('.csv'):
            G = snap.LoadEdgeList(snap.TUNGraph, datasetPath, 0, 1, ',')
        else:
            G = snap.LoadEdgeList(snap.TUNGraph, datasetPath, 0, 1, '\t')

    print("\n***********************************************************************")
    print("\nIteration ",i)
    
    startTime = time.time()
    if prob_function == "constant":
        print("\n*Edges pre-computation...(based on constant prob function with const= ",prob_const)
        edge_filtering(G, "constant", const=prob_const)
    else:
        print("\n*Edges pre-computation...(based on {} prob function".format(prob_function))
        edge_filtering(G, prob_function)
    print(f"Time taken: {round(time.time()-startTime, 2)} s")

    print("\nGraph Info after edges pre-computation:")
    print_graph_basic_info(G)
    print_graph_deg_info(G)
    print_graph_extra_info(G)

    print("\n*Treshold SETTING...")
    startTime = time.time()
    node_threshold_mapping = {}
    if treshold_function == "constant":
        print("Threshold function= constant with const ",tresholds_const)
        node_threshold_mapping = threshold_setting(G, treshold_function, const=tresholds_const)
    else:
        print("Threshold function= {} with coefficient a={} and b={} ",treshold_function,tresholds_coeff[0],tresholds_coeff[1])
        node_threshold_mapping = threshold_setting(G, treshold_function, a=tresholds_coeff[0],b=tresholds_coeff[1])
    print(f"Time taken: {round(time.time()-startTime, 2)} s")

    print("\n*TSS execution...")
    startTime = time.time()
    S = target_set_selection(G, node_threshold_mapping)
    print("Target Set Size for Iteration {} -> {}".format(i,len(S)))
    print(f"Time taken: {round(time.time()-startTime, 2)} s")
    size_S.append(len(S))

avg_S_size = math.ceil(sum(size_S)/len(size_S))
print(f"Total time taken for 10 iterations: {round(time.time()-startTotalTime, 2)} s")
print("\nAverage target set size on 10 iterations = {}".format(avg_S_size))
