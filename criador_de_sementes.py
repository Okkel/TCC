import random
import sys
import copy
from igraph import *
import time
import numpy as np

if sys.argv[2] == 'd':
	g = Graph.Read_Ncol(sys.argv[1], directed = True)
elif sys.argv[2] == 'n':
	g = Graph.Read_Ncol(sys.argv[1], directed = False)

n = 600
my_list = []
print (g.vcount())
print('grau')
a = g.degree(g.vs(), mode=ALL, loops=False)
my_list.append(a[:n])

print('betweenness')
a = g.betweenness()
my_list.append(a[:n])

print('pagerank')
a = g.pagerank(g.vs())
my_list.append(a[:n])

print('closeness')
a = g.closeness()
my_list.append(a[:n])


with open('sementes.txt', 'w') as f:
    for s in my_list:
        f.write(str(s))
        f.write('\n')
