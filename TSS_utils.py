import math
import random as rand

def print_graph_basic_info(graph):
	print("Number of nodes = {}".format(graph.GetNodes()))
	print("Number of edges = {}".format(graph.GetEdges()))

def print_graph_deg_info(graph):
	print("Max Node Degree = {}".format(graph.GetNI(graph.GetMxDegNId()).GetDeg()))

def get_graph_avg_degree(graph):
    degSum = 0
    for v in graph.Nodes():
        degSum += v.GetDeg()
        
    return math.ceil(degSum / graph.GetNodes())

def print_graph_extra_info(graph):
	print("Avg Node Degree = {}".format(get_graph_avg_degree(graph)))
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
def edge_filtering(graph, propability_function, **kwargs):
    edges_to_remove = []

    if propability_function == "random":
        for e in graph.Edges():
            if random_edge_probability_distribution() < rand.uniform(0,1):
                edges_to_remove.append((e.GetSrcNId(),e.GetDstNId()))
    elif propability_function == "constant":
        for e in graph.Edges():
            const = kwargs.get("const", None)
            if const < rand.uniform(0,1):
                edges_to_remove.append((e.GetSrcNId(),e.GetDstNId()))
    elif propability_function == "degree_based":
        for e in graph.Edges():
            if degree_based_edge_probability_distribution(graph, e) < rand.uniform(0,1):
                edges_to_remove.append((e.GetSrcNId(),e.GetDstNId()))
    else: print("The probability distribution function specified is not supported")
    
    for e in edges_to_remove:
        graph.DelEdge(e[0], e[1])


#node thresholds init setting
def threshold_setting(graph, threshold_function, **kwargs):
    node_threshold_mapping = {}
    if threshold_function == "constant":
        for v in graph.Nodes():
            const = kwargs.get("const", None)
            node_threshold_mapping[v.GetId()] = min(const,v.GetDeg()) # min(const, d(v))
    elif threshold_function == "degree_based":
        for v in graph.Nodes():
            a = kwargs.get("a", None)
            b = kwargs.get("b", None)
            node_threshold_mapping[v.GetId()] = min(math.ceil((a * v.GetDeg() / b)),v.GetDeg()) # min(t(v) = a * d(v) / b, d(v))
    else: print("The threshold function specified is not supported")

    return node_threshold_mapping

#TSS algorithm
def target_set_selection(graph, node_threshold_mapping):
    S = set()
    active_ready_set = set()
    while graph.GetNodes() > 0:
        max_node_id = -1
        max_ratio_value = -1
        node_id_to_add_to_ts = None

        for v in graph.Nodes():
            #CASE 1:if exists a node with threshold == 0 it is already active so It influences other nodes in its neighbourhood
            #and then delete it from the network 
            if node_threshold_mapping[v.GetId()] == 0: 
                active_ready_set.add(v.GetId())
            else:
                if v.GetDeg() < node_threshold_mapping[v.GetId()]:
                    #CASE 2:it exists a node that has the degree < of its threshold
                    #so add it to the target set S because having a few link nobody can influence it
                    #and then delete it from the network 
                    node_id_to_add_to_ts = v.GetId()
                else:
                    #CASE 3:pick a nod v with the selected criteria, decrement of 1 its threshold neighborhoods
                    #and then delete it from the network
                    denominator = v.GetDeg()*(v.GetDeg()+1)
                    if denominator == 0: ratio = 0
                    else: ratio = node_threshold_mapping[v.GetId()] / denominator
                    if ratio > max_ratio_value:
                        max_node_id = v.GetId()
                        max_ratio_value = ratio

        #update thresholds and node delete
        if(len(active_ready_set) > 0):
            while(len(active_ready_set) > 0):
                node_id = active_ready_set.pop()
                _,NodeVec = graph.GetNodesAtHop(node_id, 1, False) #get node's neighborhood
                for item in NodeVec:
                    #decrement of 1 the threshold of neighbors nodes still inactive
                    if node_threshold_mapping[item] > 0: node_threshold_mapping[item] -= 1

                graph.DelNode(node_id)

        else:
            if node_id_to_add_to_ts != None:
                S.add(node_id_to_add_to_ts)
                _,NodeVec = graph.GetNodesAtHop(node_id_to_add_to_ts, 1, False) #get node's neighborhood
                for item in NodeVec:
                    #decrement of 1 the threshold of neighbors nodes still inactive
                    if node_threshold_mapping[item] > 0: node_threshold_mapping[item] -= 1

                graph.DelNode(node_id_to_add_to_ts)
            else:
                graph.DelNode(max_node_id)

    return S
