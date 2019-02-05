# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 18:38:12 2019

@author: Asus
"""

import networkx as nx
from networkx import number_of_nodes
from random import randint, sample, uniform
from networkx.generators.community import caveman_graph
from networkx.generators.classic import empty_graph
import matplotlib.pyplot as plt

G=caveman_graph(1, randint(3,10))

nx.set_node_attributes(G, 0, 'wealth')
for i in G.nodes:
    G.node[i]['wealth'] = uniform(0, 1/number_of_nodes(G))
roles = ['clique denizen', 'starlead', 'starcom', 'spoke']
nx.set_node_attributes(G, roles[0], 'role')
mspokes=sample(list(G.nodes), randint(1, number_of_nodes(G)))
print(mspokes)
for j in mspokes:
    G.node[j]['role'] = roles[3]
    List = [(j+1)*100,(j+1)*101,(j+1)*102,(j+1)*103,(j+1)*104,(j+1)*105]
    RandomSample = sample(List, randint(1,6))
    f_j= empty_graph(1)
    G.add_node(f_j, wealth = uniform(0, 1/len(RandomSample)), role = roles[1])
    G.add_edge(j, f_j)
    G.add_nodes_from(RandomSample, wealth = uniform(0, 1/len(RandomSample)), role=roles[2])
    for k in RandomSample:
        G.add_edge(f_j, k)



endgame = False
coalstar = False
collapseprob = 0.99


while(endgame == False):
    
    ASetting = ['player', 'agenda setter']
    nx.set_node_attributes(G, ASetting[0] , 'setting')
    Coalition = ['None', 'Star', 'Clique']
    nx.set_node_attributes(G, Coalition[0] , 'coalition')

    for j in G.nodes():
        if G.node[j]['role'] == 'starcom':
            G.node[j]['setting'] = 'agenda setter'

    cliquelist=[]
    for i in G.nodes():
        if G.node[i]['role'] == roles[0]:
            cliquelist.append(i)
        if G.node[i]['role'] == roles[3]:
            cliquelist.append(i)
        
    counter= len(cliquelist)-1

    w=0
    ran = randint(0,counter)
    winner = cliquelist[ran]
    for i in cliquelist:
        if i == winner:
            G.node[i]['setting'] = ASetting[1]
            w = G.node[i]['wealth']
            del cliquelist[i]
            print(i)

    counter = len(cliquelist)
   
    for i in range(counter):
        R = cliquelist[i]
        w= w + G.node[R]['wealth']
        
    residual = 1 - w
    
    spokemap= {}
    for i in G.nodes:
        if G.node[i]['role'] == 'spoke':
            spokemap[i]= []
            spokemap[i].append(G.node[i]['wealth'])
            
    frac = 0
    fraclist = []
    for i in mspokes:
        i = randint(1,10)
        fraclist.append(i)
        frac = frac + i
    

    for i in range(len(fraclist)):
        fraclist[i] = fraclist[i]/frac
        

    for i in range(len(fraclist)):
        R= mspokes[i]
        gamma = fraclist[i] * residual
        spokemap[R].append(gamma)
    
    
    for i in G.nodes():
        if G.node[i]['role'] == roles[1]:
            starlist = list(G.neighbors(i))
            frac_i = 0
            fraclist_i = 0
            w_i = G.node[i]['wealth']
            G.node[i]['coalition'] == Coalition[1]
            for j in starlist:
                G.node[j]['coalition'] == Coalition[1]
                w_i = w_i + G.node[j]['wealth']
            residual_i= 1 - w_i    
            for j in starlist:
                if G.node[j]['role'] == roles[3]:
                    spokemap[j].append(residual_i)
                    if max(spokemap[j]) == spokemap[j][2]:
                        print('Success! Star ' + str(j) + ' has formed a coalition')
                        G.node[j]['coalition'] == Coalition[1]
                        endgame = True
                        coalstar = True
                        break
        if endgame:
            break
    if endgame:
        break
        
    spokecount = len(mspokes)
    spokeagree = 0
    
  
    for i in mspokes:
        if max(spokemap[i]) == spokemap[i][1]:
            spokeagree = spokeagree + 1
            G.node[i]['coalition'] == Coalition[2]

    if spokeagree == spokecount:
            print('Success! The Clique has formed a coalition!' )
            endgame = True
    else:
        if not coalstar == True:
            print('No consensus was reached. Starting over...')

    collapse = uniform(0,1)
    if collapse >= collapseprob:
        print('The process has collapsed')
        break



if coalstar == False:
    if spokeagree == spokecount:
        color_map = {'spoke':'blue', 'clique denizen':'blue', 'starcom':'red', 'starlead' : 'red'}
    else:
        color_map = {'spoke':'red', 'clique denizen':'red', 'starcom':'red', 'starlead' : 'red'}
else:
    color_map = {'spoke':'blue', 'clique denizen':'red', 'starcom':'blue', 'starlead' : 'blue'}

nx.draw(G, node_color=[color_map[G.node[node]['role']] for node in G], with_labels = True)

plt.show()
        
    

