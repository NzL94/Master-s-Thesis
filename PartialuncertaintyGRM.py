# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 18:38:12 2019

@author: Asus
"""
import csv
import networkx as nx
from networkx import number_of_nodes
from random import randint, sample, uniform
from networkx.generators.community import caveman_graph
from networkx.generators.classic import empty_graph

n = 0
cliquewin =0
starwin = 0
tie = 0

csvData = [['Outcome', 'Star', 'Avg. Star', 'Clique', 'Num' ]]

while n < 10000:

    G=caveman_graph(1, randint(3,30))

    nx.set_node_attributes(G, 0, 'wealth')
    for i in G.nodes:
        G.node[i]['wealth'] = uniform(0, 1/number_of_nodes(G))
    roles = ['clique denizen', 'starlead', 'starcom', 'spoke']
    nx.set_node_attributes(G, roles[0], 'role')
    
    mspokes=sample(list(G.nodes), randint(1, number_of_nodes(G)))
    print(mspokes)
    for j in mspokes:
        G.node[j]['role'] = roles[3]
        List = [(j+1)*100,(j+1)*101,(j+1)*102,(j+1)*103,(j+1)*104,(j+1)*105, (j+1)*106, (j+1)*107]
        RandomSample = sample(List, randint(3,8))
        f_j= empty_graph(1)
        G.add_node(f_j, wealth = uniform(0, 1/(len(RandomSample) +1)), role = roles[1])
        G.add_edge(j, f_j)
        G.add_nodes_from(RandomSample, wealth = uniform(0, 1/(len(RandomSample) +1)), role=roles[2])
        for k in RandomSample:
            G.add_edge(f_j, k)
    


    endgame = False
    collapseprob = 0.99
    tot = len(list(G.nodes()))

    while(endgame == False):
        
        coalstar = False
        coalclique = False
    
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
            gamma = fraclist[i] * residual + G.node[R]['wealth']
            spokemap[R].append(gamma)
            
        avgstar = 0
        for i in G.nodes():
            if G.node[i]['role'] == roles[1]:
                avgstar = avgstar + len(list(G.neighbors(i)))
        
        avgstar = avgstar / len(mspokes)
        
    
        for i in G.nodes():
            if G.node[i]['role'] == roles[1]:
                starlist = list(G.neighbors(i))
                frac_i = 0
                fraclist_i = 0
                w_i = G.node[i]['wealth']
                for j in starlist:
                    w_i = w_i + G.node[j]['wealth']
                residual_i= 1 - w_i    
                for j in starlist:
                    if G.node[j]['role'] == roles[3]:
                        spokemap[j].append(residual_i)
                        if max(spokemap[j]) == spokemap[j][2]:
                            print('Success! Star ' + str(j) + ' has formed a coalition')
                            starwin = starwin +1
                            n=n+1
                            coalstar = True
                            endgame = True
                            break
            if endgame:
                break
            
        
        spokecount = len(mspokes)
        spokeagree = 0
    
  
        for i in mspokes:
            if max(spokemap[i]) == spokemap[i][1]:
                spokeagree = spokeagree + 1

        if spokeagree == spokecount:
                print('Success! The Clique has formed a coalition!' )
                cliquewin = cliquewin +1
                n=n+1
                coalclique = True
                endgame = True
        else:
            if not coalstar == True:
                print('No consensus was reached. Starting over...')
        
        if not coalstar == True or coalclique == True:
            collapse = uniform(0,1)
            if collapse >= collapseprob:
                print('The process has collapsed')
                tie = tie +1
                n = n+1
                break
        
    OU = 0        
    if coalstar == False:
        if coalclique == True:
            OU = 1
        else:
            OU= 0
    else:
        OU = 2
            
    csvData.append([OU, len(mspokes), avgstar, len(cliquelist)+1, tot ])

            
        

print(n)
print(cliquewin)
print(starwin)
print(tie)


with open('person.csv', 'w') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(csvData)

csvFile.close()
 
    

