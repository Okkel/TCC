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

# Testing by degree

	# print"Testing by degree"
	# a = grafo.degree(grafo.vs(), mode=ALL, loops=False)
	# a, vindex = (list(x) for x in zip(*sorted(zip(a, vindex), reverse=True)))
	#
	# arq = open(sys.argv[1]+"degree.txt","w")
	#
	# arq.write("sementes:  "+str(vindex[:50])+"\n")
	# for i in range(10):
	#
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
	# print "\n\n <-degree"
	# arq.close()

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

	print"Testing by pagerank"

	a = grafo.pagerank(grafo.vs())
	a, vindex = (list(x) for x in zip(*sorted(zip(a, vindex), reverse=True)))
	arq = open(sys.argv[1]+"pagerank.txt","w")

	arq.write("sementes:  "+str(vindex[:50])+"\n")
	for i in range(10):
		for i in vindex[:50]:
			temp.append(i)
			temp2 = temp[:]
			l = LTM(grafo,  seeds = temp2)
			l.iniciaArestas()
			infec.append(100.0*(l.infectar())/grafo.vcount())
		print "\n",infec
		arq.write(str(infec))
		arq.write("\n")

		infec = []
		temp = []
	print "\n\n <-pagerank"
	arq.close()


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
