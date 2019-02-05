# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 12:23:35 2018

@author: Asus
"""

import networkx as nx
from networkx import number_of_nodes
from random import randint, sample, uniform
from networkx.generators.community import caveman_graph
from networkx.generators.classic import empty_graph
import matplotlib.pyplot as plt


def LHTopology(n):
    G=caveman_graph(1, randint(3,n))
    wecq=uniform(0, 1/number_of_nodes(G))
    nx.set_node_attributes(G, wecq, 'wealth')
    roles = ['clique denizen', 'starlead', 'starcom', 'spoke']
    nx.set_node_attributes(G, roles[0], 'role')
    fig, ax = plt.subplots(1, 1, figsize=(8, 6));
    mspokes=sample(list(G.nodes), randint(1, number_of_nodes(G)))
    print(mspokes)
    for j in mspokes:
        G.node[j]['role'] = roles[3]
        print(G.nodes[j]['role'])
        List = [(j+1)*100,(j+1)*101,(j+1)*102,(j+1)*103,(j+1)*104,(j+1)*105]
        RandomSample = sample(List, randint(1,6))
        west = uniform(0, 1/len(RandomSample))
        f_j= empty_graph(1)
        G.add_node(f_j, wealth = west, role = roles[1])
        G.add_edge(j, f_j)
        G.add_nodes_from(RandomSample, wealth = west, role=roles[2])
        for k in RandomSample:
            G.add_edge(f_j, k)
    nx.draw_networkx(G, ax=ax) 
    return G
