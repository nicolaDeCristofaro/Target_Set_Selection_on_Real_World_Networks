import snap
import sys
import os

from TSS_utils import *

#DEFAULT args
datasetPath = './Datasets/twitch/ENGB/musae_ENGB_edges.csv'
#datasetPath = './Datasets/git_web_ml/musae_git_edges.csv'
prob_function = "degree_based"
prob_const = ""
treshold_function = "degree_based"
tresholds_coeff = [1, 2]

if len(sys.argv) == 6 or len(sys.argv) == 7:
    print("\n TSS Execution")
    datasetPath = sys.argv[1]
    prob_function = sys.argv[2]
    if prob_function == "constant":
        prob_const = float(sys.argv[3])
        treshold_function = sys.argv[4]
        tresholds_coeff[0] = float(sys.argv[5])
        tresholds_coeff[1] = float(sys.argv[6])
        print("\t =(prob_func = {} {} \n \t   treshold_func = {} with coeff ({},{}))".format(prob_function,prob_const,treshold_function,tresholds_coeff[0],tresholds_coeff[1]))
    else:
        treshold_function = sys.argv[3]
        tresholds_coeff[0] = float(sys.argv[4])
        tresholds_coeff[1] = float(sys.argv[5])
        print("\t =(prob_func = {} \n \t   treshold_func = {} with coeff ({},{}))".format(prob_function,treshold_function,tresholds_coeff[0],tresholds_coeff[1]))
else:
    #NO params or incorrect number: DEFAULT EXECUTION
    print("TSS Execution - No params or incorrect number of params, so the DEFAULT values will be considered")
    print("\t =(prob_func = {} \n \t  treshold_func = {} with coeff ({},{}))".format(prob_function,treshold_function,tresholds_coeff[0],tresholds_coeff[1]))

# Load graph
G = snap.LoadEdgeList(snap.TUNGraph, datasetPath, 0, 1, ',')
print("\n Original Graph Info:")
print_graph_basic_info(G)
print_graph_extra_info(G)

print("\n *Edges pre-computation...")
if prob_function == "constant":
    edge_filtering(G, "constant", const=prob_const)
else:
    edge_filtering(G, prob_function)

print("\n Graph Info after edges pre-computation:")
print_graph_basic_info(G)
print_graph_extra_info(G)

#Write filtered graph on file
G.SaveEdgeList('edge_filtered_graph.txt')

#prob_func selected and applied, tresholds_func selected, now we can execute TSS
size_S = []
for i in range(0,10): #10 iterations of TSS
    if i > 0:
        #Read filtered graph from file (because graph from precent iteration is modified)
        G = snap.LoadEdgeList(snap.TUNGraph, 'edge_filtered_graph.txt', 0, 1, '\t')

    node_treshold_mapping = treshold_setting(G, treshold_function, tresholds_coeff[0],tresholds_coeff[1])

    S = target_set_selection(G, node_treshold_mapping)
    size_S.append(len(S))

avg_S_size = sum(size_S)/len(size_S)
print("\n Average target set size on 10 iterations = {}".format(round(avg_S_size,2)))
os.remove('edge_filtered_graph.txt')
