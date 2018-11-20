# coding: utf-8
# user/bin/python

#code by Arthur Rodrigues da Silva

import random
import igraph
import sys
import time
import numpy as np
from igraph import *

class LTM():   #Linear Threshhold Model

	def __init__(self,grafo, n = 50, t = 'r', seeds = None):


		self.g = grafo
		vindex = [v.index for v in self.g.vs]
		if seeds:
			self.seeds = seeds

		elif t == 'r':
			# selecting seeds randomly

			vindex = [v.index for v in self.g.vs]
			self.seeds = [random.choice(vindex) for x in range(n) ]

		elif t == 'd':

			a = self.g.degree(self.g.vs(), mode=ALL, loops=False)
			a, vindex = (list(x) for x in zip(*sorted(zip(a, vindex), reverse=True)))
			self.seeds = vindex[0:n]

		elif t == 'b':

			a = self.g.betweenness()
			a, vindex = (list(x) for x in zip(*sorted(zip(a, vindex), reverse=True)))
			self.seeds = vindex[0:n]

		elif t == 'pr':

			a = self.g.pagerank(self.g.vs())
			a, vindex = (list(x) for x in zip(*sorted(zip(a, vindex), reverse=True)))
			self.seeds = vindex[0:n]

		elif t =='cl':
			a = self.g.closeness()
			a, vindex = (list(x) for x in zip(*sorted(zip(a, vindex), reverse=True)))
			self.seeds = vindex[0:n]

		else:
			print "tipo inválido! \n"
			exit()

		self.ativos = len(self.seeds)

		self.newSeeds = []


		# print(len(self.seeds))
		#   estados:
		#   0 = inativo
		#   1 = ativo
		#   2 = ativo e nao pode ativar ninguém
		for v in self.g.vs():
			v['estado'] = 0
			v['pressao'] = 0.0
			v['theta'] = 0.0

			#ativarSementes
			if v.index in self.seeds:
				v['estado'] = 1

		# iniciar arestas
		for e in self.g.es():
			e['weight'] = 1.0


		self.g.simplify(multiple=True,combine_edges="sum")
		self.g.to_directed()

		# giving starting Threshhold value to use self.theta on mode 0
		for v in self.g.vs():
			v['theta'] = np.random.uniform(0,1)

	def iniciaArestas(self):


		self.g.vs['forca'] = self.g.strength(mode=IN, weights='weight')

		t = 0
		for v in self.g.vs():
			edges = self.g.incident(v, mode=IN)
			i = 0
			p = 0.0

			for e in edges:
				self.g.es[e]['weight'] = self.g.es[e]['weight']/v['forca']
				i+=1
				p += self.g.es[e]['weight']

			t +=i
			if abs(p - 1.000) > 0.001 and p != 0.0:
				print "p ", p, v.index, v['name'], v.degree(mode = IN)

		# print "total = ", t


	def pressionar(self,v,e):
		# v = vertex pos ,e = edge

		self.g.vs[v]['pressao'] += self.g.es[e]['weight']


		if ((self.g.vs[v]['pressao'] >= self.g.vs[v]['theta'])):
			self.g.vs[v]['estado'] = 1
			self.ativos +=1
			self.newSeeds.append(v)


	def infectar (self):
		a = 0
		# print 'infectando...'
		# print 'estado inicial:\n','seeds:',len(self.seeds)
		while a !=self.ativos:
			a = self.ativos
			for v in self.seeds:

				edge = self.g.incident(v, mode=OUT)
				for e in edge:
					if (self.g.vs[self.g.es[e].target]['estado'] == 0):
						self.pressionar(self.g.es[e].target,e)


				self.g.vs[v]['estado'] = 2
				self.seeds.remove(v)



			self.seeds.extend(self.newSeeds)
			self.newSeeds=[]

		cont = 0
		for v in self.g.vs():
			if v['estado'] != 0:
				cont += 1

		# print '\nforam ativos um total de',cont,'nos de um total de ',self.g.vcount()
		return cont

if __name__ == '__main__':


	if sys.argv[2] == 'd':
		grafo = Graph.Read_Ncol(sys.argv[1], directed = True)
	elif sys.argv[2] == 'n':
		grafo = Graph.Read_Ncol(sys.argv[1], directed = False)

	infec = []
	temp = []
	vindex = [v.index for v in grafo.vs]

## Testing by seeds

	# CA-GrQc
	# 0_grau
	s0 = [101, 295, 279, 103, 77, 72, 296, 288, 265, 100, 159, 285, 1284, 282, 302, 275, 263, 262, 269, 300, 303, 301, 277, 267, 259, 221, 297, 280, 261, 299, 294, 290, 264, 284, 273, 1037, 577, 293, 292, 291, 289, 286, 283, 278, 276, 274, 270, 266, 545, 1278]
	# 1_betweennes
	s1 = [1037, 11, 207, 53, 577, 20, 147, 186, 108, 288, 365, 244, 1088, 353, 363, 465, 346, 369, 36, 396, 545, 1066, 1515, 1032, 230, 359, 457, 2065, 214, 72, 1091, 102, 543, 146, 3137, 101, 119, 315, 44, 746, 375, 279, 45, 698, 27, 504, 1079, 41, 322, 333]
	# 2_pagerank
	s2 = [108, 1037, 577, 11, 186, 295, 53, 103, 1733, 101, 279, 1243, 1032, 450, 31, 20, 365, 457, 363, 1088, 72, 207, 288, 346, 370, 315, 369, 100, 396, 296, 2009, 1091, 465, 45, 77, 545, 244, 375, 2138, 27, 265, 984, 543, 757, 418, 398, 1066, 230, 746, 2029]
	# 3_closeness
	s3 = [1037, 147, 11, 288, 244, 101, 1515, 359, 279, 103, 322, 265, 53, 230, 20, 545, 300, 72, 353, 577, 73, 241, 36, 365, 363, 369, 282, 346, 256, 295, 214, 253, 1032, 303, 159, 77, 2182, 100, 207, 302, 44, 263, 285, 146, 296, 1066, 41, 186, 258, 262]
	# 4_eigenvector_centrality
	s4 = [101, 265, 279, 296, 77, 159, 302, 275, 285, 282, 262, 288, 295, 100, 103, 72, 301, 267, 263, 269, 297, 300, 277, 280, 264, 303, 294, 299, 261, 284, 290, 273, 293, 292, 291, 289, 286, 283, 278, 276, 274, 266, 259, 270, 271, 260, 545, 615, 622, 614]
	# 5_harmonic_centrality
	s5 = [1037, 288, 101, 279, 11, 103, 244, 147, 265, 72, 300, 295, 359, 322, 545, 1515, 77, 53, 100, 577, 282, 159, 230, 20, 296, 302, 285, 263, 73, 303, 241, 353, 262, 275, 256, 36, 277, 259, 346, 299, 365, 363, 301, 269, 253, 280, 1032, 207, 261, 369]
	# 6_load_centrality
	s6 = [1037, 207, 11, 53, 20, 577, 147, 186, 108, 1088, 288, 365, 244, 363, 465, 353, 346, 369, 396, 36, 1515, 545, 1066, 1032, 230, 457, 214, 2065, 1091, 359, 102, 146, 72, 3137, 119, 315, 746, 543, 45, 27, 375, 44, 698, 504, 279, 41, 1079, 333, 101, 15]
	# 7_PCA_all
	s7 = [1037, 577, 11, 288, 53, 207, 20, 108, 186, 101, 279, 72, 295, 103, 147, 244, 545, 365, 363, 1088, 346, 77, 100, 369, 465, 353, 396, 265, 1032, 303, 300, 1066, 282, 457, 296, 1515, 230, 36, 1091, 1733, 159, 102, 269, 2065, 1284, 359, 285, 315, 543, 375]

	# Health

	# 0_grau
	# s0 = [2055, 835, 2038, 790, 604, 2093, 2040, 131, 2151, 1936, 836, 577, 347, 1955, 707, 67, 66, 2282, 2201, 925, 494, 410, 124, 687, 607, 123, 2091, 2088, 1229, 690, 673, 644, 258, 208, 196, 1903, 1449, 1092, 931, 792, 714, 572, 395, 303, 257, 217, 205, 166, 2235, 2208]
	# # 1_betweennes
	# s1 = [101, 572, 714, 794, 1043, 1911, 1744, 741, 607, 1903, 155, 1830, 123, 132, 1321, 1936, 686, 1174, 98, 1137, 66, 268, 214, 196, 791, 995, 148, 2183, 2394, 802, 1325, 395, 1957, 329, 963, 2300, 1204, 1982, 1229, 258, 1135, 115, 1227, 1322, 1837, 2089, 986, 337, 1604, 1154]
	# # 2_pagerank
	# s2 = [835, 931, 2055, 2038, 2040, 790, 577, 66, 321, 147, 82, 2151, 2093, 617, 320, 494, 925, 580, 604, 1936, 1022, 67, 876, 165, 410, 2106, 2088, 237, 770, 495, 170, 69, 2091, 836, 1138, 703, 1449, 2094, 42, 2086, 687, 618, 806, 1034, 620, 322, 2085, 2222, 2077, 208]
	# # 3_closeness
	# s3 = [835, 147, 604, 931, 621, 607, 101, 790, 66, 687, 217, 925, 620, 170, 1449, 577, 1053, 618, 1034, 494, 240, 743, 347, 574, 596, 410, 1229, 42, 836, 69, 1204, 67, 1454, 257, 495, 741, 575, 166, 606, 792, 930, 617, 644, 432, 593, 70, 605, 1320, 243, 843]
	# # 4_eigenvector_centrality
	# s4 = [2055, 2040, 2038, 2151, 2106, 2088, 2085, 2235, 2234, 2150, 2105, 2084, 2104, 1955, 2259, 1936, 2270, 2091, 1038, 2107, 2148, 2089, 2324, 2093, 2269, 2448, 2147, 2256, 1954, 1037, 2110, 2039, 2128, 2435, 1985, 2094, 2201, 2012, 931, 2274, 2126, 2169, 2125, 2371, 2095, 835, 2271, 1061, 2374, 2282]
	# # 5_harmonic_centrality
	# s5 = [835, 604, 147, 931, 790, 607, 621, 66, 101, 687, 217, 925, 577, 620, 170, 1449, 1053, 494, 347, 410, 1034, 836, 596, 618, 67, 257, 1229, 743, 240, 1454, 69, 1204, 42, 495, 741, 574, 166, 575, 606, 1936, 2093, 580, 644, 792, 70, 930, 876, 432, 617, 339]
	# # 6_load_centrality
	# s6 = [572, 101, 714, 1043, 794, 1911, 1744, 1903, 741, 1830, 155, 123, 607, 132, 1321, 1174, 686, 1137, 1936, 268, 98, 214, 791, 66, 995, 196, 2183, 148, 802, 1325, 329, 963, 2394, 395, 1982, 1135, 258, 1957, 2300, 115, 1204, 1227, 1229, 1837, 337, 1604, 986, 1154, 1322, 2089]
	# # 7_PCA_all
	# s7 = [101, 572, 714, 835, 1936, 66, 2055, 2038, 607, 2040, 931, 604, 123, 1744, 1955, 1043, 741, 836, 794, 1903, 790, 2093, 1911, 268, 2151, 1229, 214, 620, 577, 196, 1830, 124, 147, 132, 347, 687, 208, 2086, 410, 925, 1322, 1204, 802, 131, 98, 166, 2089, 2088, 686, 791]


	seeds = [s0,s1,s2,s3,s4,s5,s6,s7]
	labels = ['0_grau','1_betweennes','2_pagerank','3_closeness','4_eigenvector_centrality','5_harmonic_centrality','6_load_centrality','7_PCA_all']
	print"Testing by seeds"

	arq = open(sys.argv[1].split('.')[0]+"__influence_seeds.txt","w")

	for j,k in zip(seeds,labels):
		for i in range(100):
			# print i

			l = LTM(grafo,  seeds = j)
			l.iniciaArestas()
			infec.append(100.0*(l.infectar())/grafo.vcount())
			temp.append(infec[-1])
		# print "\n",infec
		arq.write(str(infec))
		arq.write("\n")
		arq.write(k + "   media:   "+ str(sum(temp)/len(temp)))
		arq.write("\n")
		infec = []
		temp = []
	print "\n\n <-seeds"
	arq.close()

# Testing by betweenness

	# print"Testing by betweenness"
	#
	# a = grafo.betweenness()
	# a, vindex = (list(x) for x in zip(*sorted(zip(a, vindex), reverse=True)))
	# arq = open(sys.argv[1]+"betweenness.txt","w")
	#
	# arq.write("sementes:  "+str(vindex[:50])+"\n")
	#
	# for i in range(10):
	# 	for i in vindex[:50]:
	# 		temp.append(i)
	# 		temp2 = temp[:]
	# 		l = LTM(grafo,  seeds = temp2)
	# 		l.iniciaArestas()
	# 		infec.append(100.0*(l.infectar())/grafo.vcount())
	# 	print "\n",infec
	# 	arq.write(str(infec))
	# 	arq.write("\n")
	# 	infec = []
	# 	temp = []
	# print "\n\n <-betweenness"
	# arq.close()

# Testing by pagerank

	# print"Testing by pagerank"
	#
	# a = grafo.pagerank(grafo.vs())
	# a, vindex = (list(x) for x in zip(*sorted(zip(a, vindex), reverse=True)))
	# arq = open(sys.argv[1]+"pagerank.txt","w")
	#
	# arq.write("sementes:  "+str(vindex[:50])+"\n")
	# for i in range(10):
	# 	for i in vindex[:50]:
	# 		temp.append(i)
	# 		temp2 = temp[:]
	# 		l = LTM(grafo,  seeds = temp2)
	# 		l.iniciaArestas()
	# 		infec.append(100.0*(l.infectar())/grafo.vcount())
	# 	print "\n",infec
	# 	arq.write(str(infec))
	# 	arq.write("\n")
	#
	# 	infec = []
	# 	temp = []
	# print "\n\n <-pagerank"
	# arq.close()


# Testing by closeness

	# print"Testing by closeness"
	#
	#
	# a = grafo.closeness()
	# a, vindex = (list(x) for x in zip(*sorted(zip(a, vindex), reverse=True)))
	# arq = open(sys.argv[1]+"betweenness.txt","w")
	#
	# arq.write("sementes:  "+str(vindex[:50])+"\n")
	#
	# for i in range(10):
	# 	for i in vindex[:50]:
	# 		temp.append(i)
	# 		temp2 = temp[:]
	# 		l = LTM(grafo,  seeds = temp2)
	# 		l.iniciaArestas()
	# 		infec.append(100.0*(l.infectar())/grafo.vcount())
	# 	print "\n",infec
	# 	arq.write(str(infec))
	# 	arq.write("\n")
	# 	infec = []
	# 	temp = []
	# print "\n\n <-closeness"
	# arq.close()



	# for in range(10):
	# 	l = LTM(grafo,  seeds = betweenness)
	# 	l.iniciaArestas()
	# 	b = l.infectar()
	#
	# # print grafo.summary()
	#
	# print b/float(len(grafo.vs)),"% vertices foram ativos ->", b
