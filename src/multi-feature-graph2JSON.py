import networkx as nx
import json
import os
import itertools

'''
Function to walk int graphs presented in voices_graph and in union_graph joined.
:param voice_graphs: list of graphs 
:param union_graph: graph join of graphs in voice_graph
:param dicts: list of dictionaries
:param index_start_graph: list of the first node's index of every single graph in union_graph and in union_graph joined.
:param id_name: name to save files
'''

def dataset_creation(graphs_list, union_graph, dicts, index_start_graph, id_name):
    iteration_time = 0
    count_file_save = 0
    while iteration_time < len(union_graph):
        count_file_save = create_json_graph(iteration_time, dicts,
                                                         union_graph, index_start_graph, count_file_save, id_name)
        iteration_time = iteration_time + 1
        index = 0
        while index < len(graphs_list):
            if index_start_graph[index] < len(union_graph) - 1:
                index_start_graph[index] = index_start_graph[index] + 1
                index = index + 1
            else:
                return


def create_json_graph(iteration_time, dicts, union_graph, index_start_graph, count_file_save,
                      id_name):
    gt = nx.Graph()
    for i in index_start_graph:
        gt.add_node(i, element=union_graph.nodes[i]['element'])
    link_nodes_gt(gt, union_graph)
    graphJson = {}
    graphJson["features"] = {}
    graphJson["edges"] = []
    set_edge_list(gt, graphJson)
    set_feature_list(gt, graphJson, iteration_time, dicts, id_name)
    return gt, count_file_save


def set_edge_list(gt, graphJson):
    gt_nodes = gt.nodes
    for node1 in gt_nodes:
        for node2 in gt_nodes:
            if gt.has_edge(node1, node2):
                graphJson['edges'].append([node1, node2])


def set_feature_list(gt, graphJson, nfile, dicts, id_name):
    count = 0
    for i in range(len(dicts)):
        set_feature(gt, graphJson, dicts, i)
        save_json(graphJson, nfile, count, id_name)
        count = count + 1


def set_feature(gt, graphJson, dicts, i):
    dict_i = dicts[i]
    gt_nodes = gt.nodes
    for node1 in gt_nodes:
        node_value = gt.nodes[node1]['element'].wrapped_element.value
        duration_result = dict_i[node_value]
        graphJson["features"].update({str(node1): str(duration_result)})


def link_nodes_gt(gt, union_graph):
    gt_nodes = gt.nodes
    for node1 in gt_nodes:
        for node2 in gt_nodes:
            if union_graph.has_edge(node1, node2):
                gt.add_edge(node1, node2)


def save_json(graphJson, n_file, feature_count, n_comp):
    path = 'src/' + str(n_comp) + '/'
    subdir = path + str(n_file)
    if n_file < 10:
        subdir = path + str(0) + str(n_file)
    if not os.path.exists(path):
        os.mkdir(path)
    if not os.path.exists(subdir):
        os.mkdir(subdir)
    outfile = open(subdir + '/' + str(n_file) + str(feature_count), 'w')
    json.dump(graphJson, outfile)
