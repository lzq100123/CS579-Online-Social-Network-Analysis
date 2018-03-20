# coding: utf-8
from collections import Counter, defaultdict, deque
import copy, os
import networkx as nx

def read_graph(path):
    return nx.read_edgelist('edges.txt', delimiter='\t')


def find_best_edge(graph):
    eb = nx.edge_betweenness_centrality(graph)
    return sorted(eb.items(), key=lambda x: x[1], reverse=True)[0][0]

def writeInfo2Txt(path,files):
    with open(path,'w+',encoding='utf-8') as f:
        for indx, file in enumerate(files):
            if indx == len(files):
                f.write(str(file))
            else:
                f.write(str(file) + '\n')


def writeCom2Txt(path,files):
    with open(path,'w+',encoding='utf-8') as f:
        for file in files:
            for indx, node in enumerate(file):
                if indx == len(file):
                    f.write(str(node) + '\n')
                else:
                    f.write(str(node) + '\t')

def girvan_newman(graph, num, depth=0):
    if graph.order() == 1:
        return [graph.nodes()]    
    components = [c for c in nx.connected_component_subgraphs(graph)]
    count = 0
    while len(components) < num:
        count +=1
        edge_to_remove = find_best_edge(graph)
        graph.remove_edge(*edge_to_remove)
        components = [c for c in nx.connected_component_subgraphs(graph)]
    return [c.nodes() for c in components]

def main():
    graph = read_graph('data' + os.sep + 'User2Friendsdata.txt')
    communities = girvan_newman(graph, 4, 3)
    sum = 0
    for com in communities:
        sum += len(com)
    writeInfo2Txt('clusterresult' + os.sep + 'clusterInfo.txt',[len(communities),sum / len(communities)])
    writeInfo2Txt('clusterresult' + os.sep + 'clusters.txt',communities)

if __name__ == '__main__':
    main()

