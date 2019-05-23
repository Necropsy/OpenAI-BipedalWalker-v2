#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 15:42:09 2019

@author: necropsy
"""

### Imports ###
import gym
import numpy as np
from random import uniform
from random import randint 

#1º Implementação

### Classe do Genetico ###
class BW_AG:
    #Numero de epsodios 100
    EP = 0
    #Tamanho da população 50
    POP = 0
    #Numero de gerações 100
    GR = 0
    #Define a variavel do OpenAI
    env = 0
    #Variaveis do torneio
    tr_probabilidade = 0
    tr_num_indviduos = 0
    #Variaveis da mutação
    mt_num = 0
    
    def __init__(self, EP, POP, GR):
        self.EP = EP
        self.POP = POP
        self.GR = GR
        self.best = 0
        self.populacao = []
        self.env = gym.make('BipedalWalker-v2')
        #self.env.reset()
        self.tr_probabilidade = 0.75
        self.tr_num_indviduos = int(self.POP/2)
        self.tr_lista = []
        self.mt_num = int(self.EP/10)
    
    def acao(self):
        #return env.action_space.sample()
        return np.array([uniform(-1,1),uniform(-1,1),uniform(-1,1),uniform(-1,1)])
    
    def individuo(self):
        lista = []
        for _ in range(0,self.EP):
            lista.append(self.acao())
        lista = (lista, self.avaliacao(lista))
        return lista
    
    def avaliacao(self, lista):
        self.env.reset()
        soma = 0
        for x in range(0,self.EP):
            #self.env.render()
            action = lista[x]
            observation, reward, done, info = self.env.step(action)
            soma += reward
        self.env.close()
        return soma
    
    def init_populacao(self):
        for _ in range(0, self.POP):
            self.populacao.append(self.individuo())
        self.order_populacao()
    
    def order_populacao(self):
        self.populacao.sort(key=lambda x: x[1], reverse=True)
    
    def torneio(self):
        self.tr_lista = []
        for _ in range(0, self.tr_num_indviduos):
            a = randint(0,(self.POP-1))
            b = randint(0,(self.POP-1))
            r = uniform(0,1)
            if r < self.tr_probabilidade:
                if self.populacao[a][1] > self.populacao[b][1]:
                    self.tr_lista.append(self.populacao[a])
                else:
                    self.tr_lista.append(self.populacao[b])
            else:
                if self.populacao[a][1] > self.populacao[b][1]:
                    self.tr_lista.append(self.populacao[b])
                else:
                    self.tr_lista.append(self.populacao[a])
    
    def reproducao(self):
        i = 0
        self.torneio()
        for x in range(0, int(len(self.tr_lista)/2)):
            a = self.tr_lista[i][0]
            b = self.tr_lista[i+1][0]
            slice1 = randint(1,int(self.EP-1))
            c = np.concatenate((a[:slice1],b[slice1:]))
            d = np.concatenate((b[:slice1],a[slice1:]))
            if not randint(0,1):
                c = self.mutacao(c)
            if not randint(0,1):
                d = self.mutacao(d)
            c = (c, self.avaliacao(c))
            d = (d, self.avaliacao(d))
            self.populacao.append(c)
            self.populacao.append(d)
            i += 2
        self.order_populacao()
        self.populacao = self.populacao[:self.POP+1]
        
    def mutacao(self, lista):
        ep = self.EP-1
        for _ in range(0,self.mt_num):
            ind1 = randint(0, ep)
            ind2 = randint(0, ep)
            aux = lista[ind1]
            lista[ind1] = lista[ind2]
            lista[ind1] = aux
        return lista
    
    def init_AG(self):
        i = 0
        self.init_populacao()
        self.best = self.populacao[0]
        for _ in range(0, self.GR):
            if i%10 == 0:
                self.exec_solucao(self.best[0])
            i+=1
            print("Geração: " + str(i) + " Pontuação: " + str(self.best[1]))
            self.reproducao()
            if self.best[1] < self.populacao[0][1]:
                self.best = self.populacao[0]
        print("==================== Solução ====================")
        print("A melhor pontuação: " + str(self.best[1]))
        print("Vetor de ações:")
        print(self.best[0])
        self.exec_solucao(self.best[0])
    
    def exec_solucao(self, lista):
        self.env.reset()
        for x in range(0,self.EP):
            self.env.render()
            action = lista[x]
            observation, reward, done, info = self.env.step(action)
        self.env.close()

'''
#2º Implementação

### Classe do Genetico ###
class BW_AG:
    #Numero de epsodios 100
    EP = 0
    eps = 0
    #Tamanho da população 50
    POP = 0
    #Numero de gerações 100
    GR = 0
    #Define a variavel do OpenAI
    env = 0
    
    def __init__(self, EP, POP, GR):
        self.EP = EP
        self.eps = 0
        self.POP = POP
        self.GR = GR
        self.best = []
        self.populacao = []
        self.env = gym.make('BipedalWalker-v2')
    
    def acao(self):
        return np.array([uniform(-1,1), uniform(-1,1), uniform(-1,1), uniform(-1,1)])
    
    def individuo(self):
        return self.acao()
    
    def avaliacao(self, individuo):
        self.env.reset()
        soma = 0
        for x in range(0, self.eps):
            #self.env.render()
            action = self.best[x][0]
            observation, reward, done, info = self.env.step(action)
            soma += reward
        #self.env.render()
        action = individuo
        observation, reward, done, info = self.env.step(action)
        soma += reward
        self.env.close()
        return soma
    
    def init_populacao(self):
        self.populacao = []
        for _ in range(0, self.POP):
            individuo = self.individuo()
            self.populacao.append((individuo, self.avaliacao(individuo)))
        #self.order_populacao()
    
    def order_populacao(self):
        self.populacao.sort(key=lambda x: x[1], reverse=True)
        
    def reproducao(self):
        i = 0
        for x in range(0, int(self.POP/2)):
            a = self.populacao[i][0]
            b = self.populacao[i+1][0]
            c = np.concatenate((a[:2],b[2:]))
            d = np.concatenate((b[:2],a[2:]))
            if not randint(0,5):
                c = self.mutacao(c)
            if not randint(0,5):
                d = self.mutacao(d)
            c = (c, self.avaliacao(c))
            d = (d, self.avaliacao(d))
            self.populacao.append(c)
            self.populacao.append(d)
            i += 2
        self.order_populacao()
        
    def selecao(self):
        self.order_populacao()
        self.populacao = self.populacao[:self.POP]
        
    def mutacao(self, individuo):
        individuo[randint(0,3)] = uniform(-1,1)
        return individuo
    
    def init_AG(self):
        for _ in range(0, self.EP):
            self.init_populacao()
            for _ in range(0, self.GR):
                self.reproducao()
                self.order_populacao()
                self.selecao()
            self.best.append(self.populacao[0])
            self.eps += 1
            print("Epsodio " + str(self.eps))
    
    def mostra_solucao(self):
        print("==================== Solução ====================")
        print("Melhor Pontuação: " + str(self.best[0][1]))
        print("Vetor de Ações:")
        for x in range(0,self.EP):
            print(self.best[x][0])
    
    def exec_solucao(self):
        self.env.reset()
        for x in range(0,self.EP):
            self.env.render()
            action = self.best[x][0]
            observation, reward, done, info = self.env.step(action)
        self.env.close()
'''
'''
#3º Implementação

### Classe do Genetico ###
class BW_AG:
    #Numero de epsodios 100
    EP = 0
    #Numero de epsodios em um indivíduo
    in_ep = 0
    #Tamanho da população 50
    POP = 0
    #Numero de gerações 100
    GR = 0
    #Define a variavel do OpenAI
    env = 0
    #Variaveis do torneio
    tr_probabilidade = 0
    tr_num_indviduos = 0
    #Variaveis da mutação
    mt_num = 0
    
    def __init__(self, EP, POP, GR):
        self.EP = EP
        self.POP = POP
        self.GR = GR
        self.best = 0
        self.populacao = []
        self.env = gym.make('BipedalWalker-v2')
        #self.env.reset()
        self.tr_probabilidade = 0.55
        self.tr_num_indviduos = int(self.POP/2)
        self.tr_lista = []
        self.in_ep = 20
        self.mt_num = int(self.in_ep/2)
    
    def acao(self):
        #return env.action_space.sample()
        return np.array([uniform(-1,1),uniform(-1,1),uniform(-1,1),uniform(-1,1)])
    
    def individuo(self):
        lista = []
        for _ in range(0,self.in_ep):
            lista.append(self.acao())
        lista = (lista, self.avaliacao(lista))
        return lista
    
    def avaliacao(self, lista):
        self.env.reset()
        soma = 0
        for x in range(0,self.in_ep):
            #self.env.render()
            action = lista[x]
            observation, reward, done, info = self.env.step(action)
            soma += reward
        self.env.close()
        return soma
    
    def init_populacao(self):
        for _ in range(0, self.POP):
            self.populacao.append(self.individuo())
        self.order_populacao()
    
    def order_populacao(self):
        self.populacao.sort(key=lambda x: x[1], reverse=True)
    
    def torneio(self):
        self.tr_lista = []
        for _ in range(0, self.tr_num_indviduos):
            a = randint(0,(self.POP-1))
            b = randint(0,(self.POP-1))
            r = uniform(0,1)
            if r < self.tr_probabilidade:
                if self.populacao[a][1] > self.populacao[b][1]:
                    self.tr_lista.append(self.populacao[a])
                else:
                    self.tr_lista.append(self.populacao[b])
            else:
                if self.populacao[a][1] > self.populacao[b][1]:
                    self.tr_lista.append(self.populacao[b])
                else:
                    self.tr_lista.append(self.populacao[a])
    
    def reproducao(self):
        i = 0
        self.torneio()
        for x in range(0, int(len(self.tr_lista)/2)):
            a = self.tr_lista[i][0]
            b = self.tr_lista[i+1][0]
            slice1 = randint(1,int(self.in_ep-1))
            #print("==============================")
            #print(a[:slice1])
            c = np.concatenate((a[:slice1],b[slice1:]))
            d = np.concatenate((b[:slice1],a[slice1:]))
            if not randint(0,2):
                c = self.mutacao(c)
            if not randint(0,2):
                d = self.mutacao(d)
            c = (c, self.avaliacao(c))
            d = (d, self.avaliacao(d))
            self.populacao.append(c)
            self.populacao.append(d)
            i += 2
        self.order_populacao()
        self.populacao = self.populacao[:self.POP+1]
        
    def mutacao(self, lista):
        ep = self.in_ep-1
        for _ in range(0,self.mt_num):
            ind1 = randint(0, ep)
            ind2 = randint(0, ep)
            aux = lista[ind1]
            lista[ind1] = lista[ind2]
            lista[ind1] = aux
        return lista
    
    def init_AG(self):
        i = 0
        self.init_populacao()
        self.best = self.populacao[0]
        for _ in range(0, self.GR):
            if i%10 == 0:
                self.exec_solucao(self.best[0])
            i+=1
            print("Geração: " + str(i) + " Pontuação: " + str(self.best[1]))
            self.reproducao()
            if self.best[1] < self.populacao[0][1]:
                self.best = self.populacao[0]
        print("==================== Solução ====================")
        print("A melhor pontuação: " + str(self.best[1]))
        print("Vetor de ações:")
        print(self.best[0])
        self.exec_solucao(self.best[0])
    
    def exec_solucao(self, lista):
        for _ in range(0,int(self.EP/self.in_ep)):
            lista = np.concatenate((lista, lista), axis=0)
        self.env.reset()
        for x in range(0,self.EP):
            self.env.render()
            action = lista[x]
            observation, reward, done, info = self.env.step(action)
        self.env.close()
'''
#Execução: EP/POP/GR
genetico = BW_AG(300, 200, 500)
genetico.init_AG()
genetico.mostra_solucao()
genetico.exec_solucao()