import snap
import sys
import os

from tss_utils import *

datasetPath = ""
if len(sys.argv) > 1:
    datasetPath = sys.argv[1]
else:
    sys.exit("Dataset path has to be specified") 

#datasetPath = './Datasets/twitch/ENGB/musae_ENGB_edges.csv'
#datasetPath = './Datasets/git_web_ml/musae_git_edges.csv'

G = snap.LoadEdgeList(snap.TUNGraph, datasetPath, 0, 1, ',')
print_graph_basic_info(G)
print_graph_extra_info(G)

prob_functions = ["constant","random","degree_based"]
prob_constants = [0.5,0.8]

tresholds_functions = ["constant","degree_based"]
tresholds_coeff = [(1,1),(1,2),(3,2)] # (a,b) -> q = b/(a+b)

i = 0
for prob_func in prob_functions:
    if prob_func == "constant":
        edge_filtering(G, prob_func, const=prob_constants[i])
        i += 1
    else:
        edge_filtering(G, prob_func)

    #Write filtered graph on file
    G.SaveEdgeList('edge_filtered_graph.txt')
    i = 0
    for tresholds_func in tresholds_functions:
        #Read filtered graph on file
        G = snap.LoadEdgeList(snap.TUNGraph, 'edge_filtered_graph.txt', 0, 1, '\t')
        node_treshold_mapping = treshold_setting(G, tresholds_func, tresholds_coeff[i][0],tresholds_coeff[i][1])
        i += 1

        #prob_func selected, tresholds_func selected, now we can execute TSS
        size_S = []
        for i in range(0,1):
            S = target_set_selection(G, node_treshold_mapping)
            size_S.append(len(S))
        
        avg_S_size = sum(size_S)/len(size_S)
        print("The average target set size for execution with")
        print("Probability Distribution function = {}".format(prob_func))
        print("Tresholds function = {}".format(tresholds_func))
        print("is = {}".format(round(avg_S_size,2)))
    
    #Read original graph 
    G = snap.LoadEdgeList(snap.TUNGraph, datasetPath, 0, 1, ',')

os.remove('edge_filtered_graph.txt')





