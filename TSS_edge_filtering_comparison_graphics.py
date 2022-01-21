import snap
import matplotlib.pyplot as plt
import numpy as np 

from TSS_utils import *

#Probability distribution functions to compare: constant=0.2, constant=0.6, random, degree_based
prob_constants = [0.2,0.6]

# Twitch Dataset Edge filtering comparison graphic generation
twitchDatasetPath = './Datasets/twitch/ENGB/musae_ENGB_edges.csv'
G1 = snap.LoadEdgeList(snap.TUNGraph, twitchDatasetPath, 0, 1, ',')
G1original_edges_num = G1.GetEdges()

edge_filtering(G1, "constant", const=prob_constants[0])
G1costant0_edges_num = G1.GetEdges()

G1 = snap.LoadEdgeList(snap.TUNGraph, twitchDatasetPath, 0, 1, ',')
edge_filtering(G1, "constant", const=prob_constants[1])
G1costant1_edges_num = G1.GetEdges()

G1 = snap.LoadEdgeList(snap.TUNGraph, twitchDatasetPath, 0, 1, ',')
edge_filtering(G1, "random")
G1random_edges_num = G1.GetEdges()

G1 = snap.LoadEdgeList(snap.TUNGraph, twitchDatasetPath, 0, 1, ',')
edge_filtering(G1, "degree_based")
G1degree_based_edges_num = G1.GetEdges()


# CA-GrQc Dataset Edge filtering comparison graphic generation
grQckDatasetPath = './Datasets/Arxiv_GR-QC/CA-GrQc.txt'

G2 = snap.LoadEdgeList(snap.TUNGraph, grQckDatasetPath, 0, 1, '\t')
G2original_edges_num = G2.GetEdges()

edge_filtering(G2, "constant", const=prob_constants[0])
G2costant0_edges_num = G2.GetEdges()

G2 = snap.LoadEdgeList(snap.TUNGraph, grQckDatasetPath, 0, 1, '\t')
edge_filtering(G2, "constant", const=prob_constants[1])
G2costant1_edges_num = G2.GetEdges()

G2 = snap.LoadEdgeList(snap.TUNGraph, grQckDatasetPath, 0, 1, '\t')
edge_filtering(G2, "random")
G2random_edges_num = G2.GetEdges()

G2 = snap.LoadEdgeList(snap.TUNGraph, grQckDatasetPath, 0, 1, '\t')
edge_filtering(G2, "degree_based")
G2degree_based_edges_num = G2.GetEdges()

# CA-HepTh Dataset Edge filtering comparison graphic generation
hepThDatasetPath = './Datasets/Arxiv_HEP-TH/CA-HepTh.txt'

G3 = snap.LoadEdgeList(snap.TUNGraph, hepThDatasetPath, 0, 1, '\t')
G3original_edges_num = G3.GetEdges()

edge_filtering(G3, "constant", const=prob_constants[0])
G3costant0_edges_num = G3.GetEdges()

G3 = snap.LoadEdgeList(snap.TUNGraph, hepThDatasetPath, 0, 1, '\t')
edge_filtering(G3, "constant", const=prob_constants[1])
G3costant1_edges_num = G3.GetEdges()

G3 = snap.LoadEdgeList(snap.TUNGraph, hepThDatasetPath, 0, 1, '\t')
edge_filtering(G3, "random")
G3random_edges_num = G3.GetEdges()

G3 = snap.LoadEdgeList(snap.TUNGraph, hepThDatasetPath, 0, 1, '\t')
edge_filtering(G3, "degree_based")
G3degree_based_edges_num = G3.GetEdges()

#create graphic about edge filtering
N = 3
ind = np.arange(N) 
width = 0.15

plt.figure(figsize=(15,10))

Yoriginal = [G1original_edges_num,G2original_edges_num,G3original_edges_num]
bar1 = plt.bar(ind, Yoriginal, width, color = '#442288')

Zconstant0 = [G1costant0_edges_num,G2costant0_edges_num,G3costant0_edges_num]
bar2 = plt.bar(ind+width, Zconstant0, width, color = '#6CA2EA')

Hconstant1 = [G1costant1_edges_num,G2costant1_edges_num,G3costant1_edges_num]
bar3 = plt.bar(ind+(width*2), Hconstant1, width, color = '#B5D33D')

Wrandom = [G1random_edges_num,G2random_edges_num,G3random_edges_num]
bar4 = plt.bar(ind+(width*3), Wrandom, width, color = '#FED23F')

Jdegree = [G1degree_based_edges_num,G2degree_based_edges_num,G3degree_based_edges_num]
bar5 = plt.bar(ind+(width*4), Jdegree, width, color = '#EB7D5B')

plt.xlabel("Datasets")
plt.ylabel('Number of Edges')
plt.title("Edge filtering based on different probability distribution functions")

plt.xticks(ind+width,['Twitch Dataset','CA-GrQc Dataset','CA-HepTh Dataset'])
plt.legend( (bar1, bar2, bar3, bar4, bar5), ('Original', 'Const 0.2', 'Const 0.6', 'Random', 'Degree_Based') )
plt.savefig("./graphics/edges_precomputation_comparison.png")