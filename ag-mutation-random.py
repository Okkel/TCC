# coding: utf-8
# user/bin/python

# code by Arthur Rodrigues da Silva
import random
import sys
import copy
from igraph import *
from LinearThreshold import LTM
import time
import numpy as np
import pickle
import pandas as pd
import os


class Ag():
    def __init__(self, g, len_gen, len_population, mutation, times, seeds):
        self.g = g
        self.len_gen = len_gen
        self.len_population = len_population
        self.mutation_chance = mutation
        self.population = []
        self.best_fit = 0
        self.times = times
        self.generation_cont = 0
        self.starting_seeds = seeds
        self.population.append([seeds, 0])
        print '\n\n','len_gen',self.len_gen,'len_population',self.len_population,'mutation_chance',self.mutation_chance,'times',self.times
        print 'stating_seeds',self.starting_seeds


        # try:
        #     with open('sementes.txt', 'rb') as f:
        #         all_lines = pickle.load(f)
        #         if len(all_lines) == 1:
        #             self.population.append([all_lines, 0])
        #         else:
        #             print(len(all_lines),' conjunto(s) de sementes encontrado(s)')
        #             for i in all_lines:
        #                 self.population.append([i, 0])

            # my_list = []
            # with open('sementes.txt', 'r') as f:
            #     for line in f:
            #         x = line.replace("[", "")
            #         x = x.replace("]", "")
            #         x = x.replace("\n", "")
            #         x = x.replace(",", " ")
            #         my_list.append(x)
            #
            # all_lines = [[int(num) for num in line.split()]
            #              for line in my_list]
            # if len(all_lines) == 1:
            #     self.population.append([all_lines, 0])
            #     print "all_lines ", len(all_lines)
            # else:
            #     print "all_lines maiorzinha: ", len(all_lines)
            #
            #     for i in all_lines:
            #         self.population.append([i, 0])
        # except BaseException:
        #     print "Arquivo de sementes (sementes.txt) nao enontrado \n nenhuma perturbacao da populacao inicial sera feita"

    def gen(self):  # creating a gen
        gen = random.sample(range(self.g.vcount()), self.len_gen)

        return [gen, 0]  # return (gen array , fitness)

    def best(self):
        b = 0
        for i in self.population:
            if i[1] > b:
                b = i[1]
        return b

    def new_population(self, flag=0):  # creating the population
        if flag == 0:
            # creating the first generation
            for i in range(self.len_population):
                self.population.append(self.gen())

            # if self.seeds:
            #     self.population.append(self.seeds)

            print "primeira populacao criada___________________________________"
            self.generation_cont += 1

            return

        if flag == 1:
            next_population = []
            # elitism selection
            # the best of the last generation must survive
            a = []
            best = self.best()
            for i in self.population:
                if (i[1] == best):
                    a = i[:]
                    # print "trocando",self.best_fit[1],"por",a[1]

            next_population.append(a)

            # print "reproduzindo..."
            for i in range(self.len_population / 2):
                s = self.select_parents()  # this function returns 2 sons
                # print "a",a,"******"
                next_population.append(s[0])
                next_population.append(s[1])
            self.population = next_population[:]
            # if a in self.population:
            #     print "********True*******"
            # self.population = copy.deepcopy(next_population)
            self.generation_cont += 1
            print "geracao ", self.generation_cont, " criada_______________________________________________"

            return

    def fitness(self):
        # print self.population

        temp = copy.deepcopy(self.population)

        for i in range(1, len(temp)):
            seeds = temp[i][0]
            # l = LTM(self.g,seeds)
            l = LTM(self.g, n=50, seeds=seeds)
            l.iniciaArestas()
            self.population[i][1] = (l.infectar())

        return

    def cross(self, gen1, gen2):
        interval = sorted(random.sample(range(1,len(gen1[0])-1),2))

        first_son = [gen2[0][0:interval[0]] + gen1[0][interval[0]:interval[1]] + gen2[0][interval[1]:],0]
        second_son = [gen1[0][0:interval[0]] + gen2[0][interval[0]:interval[1]] + gen1[0][interval[1]:],0]

        return (first_son,second_son)

    def select_parents(self):
        # selection strategy: tournament
        # print "selecionando pais" ,len(self.population),"->", self.best_fit[1]
        temp = random.sample(self.population, 2)

        if temp[0][1] >= temp[1][1]:
            parent1 = temp[0]
        else:
            parent1 = temp[1]

        temp = random.sample(self.population, 2)

        if temp[0][1] >= temp[1][1]:
            parent2 = temp[0]
        else:
            parent2 = temp[1]

        while parent1 == parent2:
            temp = random.sample(self.population, 2)
            parent2 = (temp[0] if temp[0][1] >= temp[1][1] else temp[1])

        a = self.cross(parent1, parent2)
        # print a,"*********************---------------------"
        return a

    def mutation(self):

        for i in range(1, len(self.population)):
            if (random.random() <= self.mutation_chance):

                pos = random.randint(1, self.len_gen - 1)

                subst = random.randint(0, self.g.vcount() - 1)
                self.population[i][0][pos] = subst

        return

    def run(self):
        saida = []
        # arq = open("fitness_evolution.txt","w")

        # generation 1
        self.new_population()
        self.fitness()

        best_fit_of_iteration = self.best()
        # calcula porcentagem de nos ativados
        saida.append((100.0 * (best_fit_of_iteration)) / float(self.g.vcount()))
        # arq.write(str((100.0*(best_fit_of_iteration))/self.g.vcount())+"\n")

        # generation 2
        self.new_population(1)


        while True:

            self.mutation()
            self.fitness()

            self.best_fit = self.best()
            saida.append((100.0 * (best_fit_of_iteration)) / float(self.g.vcount()))
            # arq.write(str((100.0*(self.best_fit))/self.g.vcount())+"\n")

            if self.generation_cont < self.times:

                print "melhor da populacao", best_fit_of_iteration, "melhor geral", self.best_fit
                if best_fit_of_iteration < self.best_fit:
                    best_fit_of_iteration = self.best_fit
                else :
                    self.best_fit = best_fit_of_iteration
                # print "nova populacao criada____________________________________",len(self.population)
                self.new_population(1)
                # cont += 1
            else:
                # arq.close()
                # print "End, best_fit", self.best_fit#,"melhor da
                # iteracao",best_fit_of_iteration

                return (saida, self.population[0])


# g.to_undirected(mode="each", combine_edges=None)
if sys.argv[2] == 'd':
    g = Graph.Read_Ncol(sys.argv[1], directed=True)
elif sys.argv[2] == 'n':
    g = Graph.Read_Ncol(sys.argv[1], directed=False)
# try:
#     with open(sys.argv[3], 'rb') as f:
#         all_lines = pickle.load(f)
#         print 'arquivo: ',sys.argv[3],' encontrado'
#         print len(all_lines)," conjuntos de sementes"
#
#
# except BaseException:
#     print "Arquivo de sementes ("+sys.argv[3]+") nao enontrado \n nenhuma perturbacao da populacao inicial sera feita"

# for li in range(len(all_lines)):
for li in range(1):
    print "\n\n executando conjunto", li
    fit_evolution = {}
    seeds_response = {}

    if not os.path.exists("fitness_evolution randon mutation" + sys.argv[1].split('.')[0]):
        os.makedirs("fitness_evolution randon mutation" + sys.argv[1].split('.')[0])
    arq = open("fitness_evolution" + sys.argv[1].split('.')[0] + "/fitness_evolution" + sys.argv[1].split('.')[0] + "_medida_"+ str(li) +".txt", "w")

    begin = time.time()
    for i in range(10):
        print "\n\n", i, "\n\n"
        a = Ag(g, 50, 50, 0.1, 100, None)
        r = a.run()
        arq.write(str(r[0]))  # crescimento de influencia em procentagem
        arq.write("\n")
        arq.write(str(r[1]))  # sementes que alcancaram melhor resultado
        arq.write("\n")
        fit_evolution[i] = r[0]
        seeds_response[i] = r[1][0] # sementes: [[sementes]. fitness] pegando apenas as sementes

    end = time.time()
    print '\n fit_evolution \n',fit_evolution
    print '--'*15
    print 'seeds_response \n',seeds_response
    df = pd.DataFrame(data=fit_evolution)
    print df.head()


    df['average'] = df[df.columns].sum(numeric_only=True, axis=1)/len(df.columns)
    print 'numero de colunas ',df.columns
    df.to_csv("fitness_evolution" + sys.argv[1].split('.')[0] +"/fitness_evolution" + sys.argv[1].split('.')[0] + "_medida_"+ str(li) +".csv",sep=';', encoding='utf-8')

    df2 = pd.DataFrame(data=seeds_response)
    df2.to_csv("fitness_evolution" + sys.argv[1].split('.')[0] +"/seeds_response" + sys.argv[1].split('.')[0] + "_medida_"+ str(li) +".csv",sep=';', encoding='utf-8')

    print "melhor resultado encontrado:\n", r, "tempo:", end - begin, "\n\n"
    fit_evolution = {}
    seeds_response = {}

    arq.close()
