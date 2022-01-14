import random as rand

def print_graph_basic_info(graph):
	print("Number of nodes = {}".format(graph.GetNodes()))
	print("Number of edges = {}".format(graph.GetEdges()))

def print_graph_extra_info(graph):
	print("Max Node Degree = {}".format(graph.GetNI(graph.GetMxDegNId()).GetDeg()))
	print("Clustering coefficient = {}".format(graph.GetClustCf()))

#probability distribution functions

#1. Random probability distribution
def random_edge_probability_distribution():
    return rand.uniform(0,1)

#2. Degree based probability distribution
def degree_based_edge_probability_distribution(graph, edge):
    source_node = graph.GetNI(edge.GetSrcNId())
    dest_node = graph.GetNI(edge.GetDstNId())
    source_node_degree = source_node.GetDeg()
    dest_node_degree = dest_node.GetDeg()

    return (1 - (1/(source_node_degree+dest_node_degree)))

#3. Constant probability distribution


#edges removals based on probability
def edge_filtering(graph, propability_function, const):
    edges_to_remove = []

    if propability_function == "random":
        for e in graph.Edges():
            if random_edge_probability_distribution() < rand.uniform(0,1):
                edges_to_remove.append((e.GetSrcNId(),e.GetDstNId()))
    elif propability_function == "constant":
        for e in graph.Edges():
            if const < rand.uniform(0,1):
                edges_to_remove.append((e.GetSrcNId(),e.GetDstNId()))
    elif propability_function == "degree_based":
        for e in graph.Edges():
            if degree_based_edge_probability_distribution(graph, e) < rand.uniform(0,1):
                edges_to_remove.append((e.GetSrcNId(),e.GetDstNId()))
    else: print("The probability distribution function specified is not supported")
    
    for e in edges_to_remove:
        graph.DelEdge(e[0], e[1])


#node tresholds init setting
def treshold_setting(graph, treshold_function, a,b):
    node_treshold_mapping = {}
    if treshold_function == "constant":
        for v in graph.Nodes():
            node_treshold_mapping[v.GetId()] = (b / (a+b)) # t(v) = b/(a+b)
    elif treshold_function == "degree_based":
        for v in graph.Nodes():
            node_treshold_mapping[v.GetId()] = (a * v.GetDeg() / b) # t(v) = a * degree(v) / b
    else: print("The treshold function specified is not supported")

    return node_treshold_mapping

#tss algorithm
def target_set_selection(graph, node_treshold_mapping):
    S = set()
    already_active_set = set()
    while graph.GetNodes() > 0:
        max_node_id = -1
        max_ratio_value = -1
        node_id_to_add_to_ts = None

        for v in graph.Nodes():
            #if exists a node with treshold == 0 it is already active so It influences other nodes in its neighbourhood
            #and then delete it from the network 
            if node_treshold_mapping[v.GetId()] == 0: 
                already_active_set.add(v.GetId())
            else:
                if v.GetDeg() < node_treshold_mapping[v.GetId()]:
                    #it exists a node that has the degree < of its treshold
                    #so add it to the target set S because having a few link nobody can influence it
                    #and then delete it from the network 
                    node_id_to_add_to_ts = v.GetId()
                else:
                    #pick a nod v with the selected criteria, decrement of 1 its treshold neighborhoods
                    #and then delete it from the network
                    ratio = node_treshold_mapping[v.GetId()] / (v.GetDeg()*(v.GetDeg()+1))
                    if ratio > max_ratio_value:
                        max_node_id = v.GetId()
                        max_ratio_value = ratio
        
        ##update tresholds
        if(len(already_active_set) > 0):
            while(len(already_active_set) > 0):
                node_id = already_active_set.pop()
                _,NodeVec = graph.GetNodesAtHop(node_id, 1, False) #get node's neighborhood
                for item in NodeVec:
                    #decrement of 1 the treshold of neighbors nodes still inactive
                    if node_treshold_mapping[item] > 0: node_treshold_mapping[item] -= 1
                
                graph.DelNode(node_id)
        
        else:
            if node_id_to_add_to_ts != None:
                S.add(node_id_to_add_to_ts)
                _,NodeVec = graph.GetNodesAtHop(node_id_to_add_to_ts, 1, False) #get node's neighborhood
                for item in NodeVec:
                    #decrement of 1 the treshold of neighbors nodes still inactive
                    if node_treshold_mapping[item] > 0: node_treshold_mapping[item] -= 1

                graph.DelNode(node_id_to_add_to_ts)
            else:
                graph.DelNode(max_node_id)

    return S



