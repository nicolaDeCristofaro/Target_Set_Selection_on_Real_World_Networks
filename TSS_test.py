import snap

from tss_utils import *

#Test 1 iteration of TSS algorithm on a simple generated graph

G = snap.TUNGraph.New() # Create UNoriented graph 
G.AddNode(1) # Add nodes 
G.AddNode(2)
G.AddNode(3)
G.AddNode(4)
G.AddNode(5)
G.AddNode(6)
G.AddNode(7)
G.AddNode(8)

G.AddEdge(1,2) # Add edges
G.AddEdge(1,4)

G.AddEdge(2,3)
#G.AddEdge(2,1)
G.AddEdge(2,5)
G.AddEdge(2,6)

#G.AddEdge(3,2)
G.AddEdge(3,6)

#G.AddEdge(4,1)
G.AddEdge(4,5)
G.AddEdge(4,7)

#G.AddEdge(5,2)
#G.AddEdge(5,4)
G.AddEdge(5,6)
G.AddEdge(5,7)

#G.AddEdge(6,3)
#G.AddEdge(6,5)
G.AddEdge(6,8)

#G.AddEdge(7,4)
#G.AddEdge(7,5)
G.AddEdge(7,8)

print_graph_basic_info(G)
print_graph_extra_info(G)

tresholds_coeff = [(2,-4)] # (a,b) -> q = b/(a+b)
node_treshold_mapping = treshold_setting(G, "constant",tresholds_coeff[0][0],tresholds_coeff[0][1])

S = target_set_selection(G, node_treshold_mapping)

print(S)