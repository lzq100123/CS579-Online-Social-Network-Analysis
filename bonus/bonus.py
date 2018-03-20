import networkx as nx
  
def jaccard_wt(graph, node):
    """
  The weighted jaccard score, defined above.
  Args:
    graph....a networkx graph
    node.....a node to score potential new edges for.
  Returns:
    A list of ((node, ni), score) tuples, representing the 
              score assigned to edge (node, ni)
              (note the edge order)
  """
    nodenb = [n for n in graph.neighbors(node)]
    node_degree = 1 / sum([graph.degree(n) for n in nodenb])
    nodelist = [n for n in graph.nodes() if n not in nodenb and n != node]
    score = []
    for n in nodelist:
        nnb = [nei for nei in graph.neighbors(n)]
        nnb_degree = 1 / sum([graph.degree(nd) for nd in nnb])
        intersection = set(nnb).intersection(set(nodenb))
        inter_degree = sum([1 / graph.degree(nd) for nd in intersection])
        sc = inter_degree / (node_degree + nnb_degree)
        score.append(((node,n),sc))
    return score  