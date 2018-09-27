import random
import sys
import copy
from igraph import *
import time
import numpy as np
import pickle
import networkx as nx


if sys.argv[2] == 'd':
	g = Graph.Read_Ncol(sys.argv[1], directed = True)
	nxg = nx.DiGraph()
	for line in g.get_edgelist():
		nxg.add_edge(line[0],line[1])
	print 'rede direcionada',sys.argv[1].split('.')[0]
elif sys.argv[2] == 'n':
	g = Graph.Read_Ncol(sys.argv[1], directed = False)
	nxg = nx.Graph()
    	for line in g.get_edgelist():
        	nxg.add_edge(line[0],line[1])	
	print 'rede nao direcionada',sys.argv[1].split('.')[0]


all_lines = []
my_list = []
print('grau')
a = nx.degree_centrality(nxg).values()
my_list.append(a)

print('betweennes')
a = nx.betweenness_centrality(nxg).values()
my_list.append(a)

print('pagerank')
a = nx.pagerank(nxg).values()
my_list.append(a)

print('closeness')
a = nx.closeness_centrality(nxg).values()
my_list.append(a)

print('eigenvector_centrality')
a = nx.eigenvector_centrality(nxg).values()
my_list.append(a)

print('harmonic_centrality')
a = nx.harmonic_centrality(nxg).values()
my_list.append(a)

print('load_centrality')
a = nx.load_centrality(nxg).values()
my_list.append(a)

for i in my_list:
    print (len(i))

with open('centralidades-'+sys.argv[1].split('.')[0]+'-picke.txt', 'wb') as f:
    pickle.dump(my_list, f)
with open('sementes.txt', 'w') as f:
    for s in my_list:
        f.write(str(s))
        f.write('\n')
