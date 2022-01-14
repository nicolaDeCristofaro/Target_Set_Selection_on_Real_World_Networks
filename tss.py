import snap

from tss_utils import *

path = './Datasets/twitch/ENGB/musae_ENGB_edges.csv'
#path = './Datasets/git_web_ml/musae_git_edges.csv'

G = snap.LoadEdgeList(snap.TUNGraph, path, 0, 1, ',')

G.PrintInfo()

"""
size_S = []
for i in range(0,5):
    path = './Datasets/twitch/ENGB//musae_ENGB_edges.csv'
    graph = snap.LoadEdgeList(snap.TUNGraph, path, 0, 1, ',')

    graph.PrintInfo()

    prob_constants = [0.5,0.8]
    edge_filtering(graph, "constant", prob_constants[2])

    graph.PrintInfo()

    tresholds_coeff = [(1,1),(1,2),(3,2)] # (a,b) -> q = b/(a+b)
    node_treshold_mapping = treshold_setting(graph, "degree_based",tresholds_coeff[0][0],tresholds_coeff[0][1])

    S = target_set_selection(graph, node_treshold_mapping)
    size_S.append(len(S))

print(size_S)
avg = sum(size_S)/len(size_S)
print("The average is ", round(avg,2))
"""

