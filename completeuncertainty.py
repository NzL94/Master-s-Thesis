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

G=caveman_graph(1, randint(3,30))

nx.set_node_attributes(G, 0, 'wealth')
for i in G.nodes:
    G.node[i]['wealth'] = uniform(0, 1/number_of_nodes(G))
roles = ['clique denizen', 'starlead', 'starcom', 'spoke']
nx.set_node_attributes(G, roles[0], 'role')
fig, ax = plt.subplots(1, 1, figsize=(8, 6));
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
nx.draw_networkx(G, ax=ax) 


endgame = False
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
            if G.node[i]['role'] == 'spoke':
                appendix = 0
            w = G.node[i]['wealth']
            del cliquelist[i]
            print(i)

    counter = len(cliquelist)
    print(cliquelist)
    offerlist=[]   
    
    for i in range(counter):
        i = randint(1,10)
        offerlist.append(i)
        w= w+i
 

    for i in range(len(offerlist)):
        offerlist[i] = offerlist[i]/w

    spokemap= {}
    for i in G.nodes:
        if G.node[i]['role'] == 'spoke':
            spokemap[i]= []
            if G.node[i]['setting'] == ASetting[1]:
                spokemap[i].append(appendix)

    wealthlist=[]
    for i in cliquelist:
        if G.node[i]['setting'] == ASetting[0]:
            if G.node[i]['role'] == roles[0]:
                wealthlist.append(G.node[i]['wealth'])
            else: 
                wealthlist.append(G.node[i]['wealth'])
                spokemap[i].append(G.node[i]['wealth'])
    
        
    for i in range(counter):
        R = cliquelist[i]
        if G.node[R]['role'] == roles[0]:
            if offerlist[i] >= wealthlist[i]:
                G.node[R]['coalition'] = Coalition[2]
        else:
            spokemap[R].append(offerlist[i])

    consenscount = 0
    denizencount = 0

    for i in cliquelist:
        if G.node[i]['coalition'] == Coalition[2]:
            consenscount = consenscount +1 
        if G.node[i]['role'] == roles[0]:
            denizencount = denizencount +1
        
    if denizencount == consenscount:
        nospokes = True
        print('There is consensus in the clique, now let us check the spokes...')
    else:
        nospokes= False
        print('There is disagreement in the clique, let us turn to the stars...')
    
    for i in G.nodes():
        if G.node[i]['role'] == roles[1]:
            starlist = list(G.neighbors(i))
            counter_i = len(starlist) -1
            w_i = G.node[i]['wealth']
            wealthlist_i = []
            offerlist_i = []
            agrcount_i = 0
            starcount_i = 0
            for j in range(counter_i):
                j = randint(1,10)
                offerlist_i.append(j)
                w_i = w_i + j
            for j in range(len(offerlist_i)):
                offerlist_i[j] = offerlist_i[j]/w_i            
            for j in starlist:
                wealthlist_i.append(G.node[j]['wealth'])  
            for j in range(counter_i):
                R_i = starlist[j]
                if G.node[R_i]['role'] == roles[2]:
                    if offerlist_i[j] >= wealthlist_i [j]:
                        G.node[R_i]['coalition'] = Coalition[1]
                else:
                    spokemap[R_i].append(offerlist[j])
            for j in starlist:
                if G.node[j]['coalition'] == Coalition[1]:
                    agrcount_i = agrcount_i +1 
                if G.node[j]['role'] == roles[2]:
                    starcount_i = starcount_i +1
            if starcount_i == agrcount_i:
                for j in starlist:
                    if G.node[j]['role'] == roles[3]:
                        if max(spokemap[j]) == spokemap[j][2]:
                            print('Success! Star ' +str(j) + ' has formed a coalition')
                            endgame = True
                            break
                        else:
                            print('Failed to convince the spoke')
            else:
                print('This star has failed to form a coalition')
            if endgame:
                break
        if endgame:
            break
        
        
    spokecount = len(mspokes)
    spokeagree = 0
    for i in G.nodes():
        if G.node[i]['role'] == roles[3]:
            if max(spokemap[i]) == spokemap[i][1]:
                pokeagree = spokeagree + 1

    if nospokes == True:
        if spokeagree == spokecount:
            print('Success! The Clique has formed a coalition!' )
            endgame = True
        else:
            print('No consensus was reached. Starting over...')
    else:
        print('No consensus was reached. Starting over...')

    collapse = uniform(0,1)
    if collapse >= collapseprob:
        print('The process has collapsed')
        break




        
    

