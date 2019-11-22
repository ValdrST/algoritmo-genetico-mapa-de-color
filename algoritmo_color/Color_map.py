from Genetica import Genetica
import numpy as np
import random
import matplotlib.pyplot as plt
import threading
class Color_map(Genetica):
    def __init__(self,prob_cruza=0.8,prob_mut=0.1,porcentaje_elite=0.1,poblacion=100,generaciones=100, fitness_min = 0.9,tam_x=16,tam_y=16):
        Genetica.__init__(self,prob_cruza,prob_mut,porcentaje_elite,poblacion,generaciones,fitness_min)
        self.tam_x = tam_x
        self.tam_y = tam_y
        self.rand_colors_dict = [(0,0,255),(0,255,255),(255,0,255),(0,255,0),(255,0,0)]
    
    @staticmethod
    def gen_random_color():
        return (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    
    def gen_random_individuo(self):
        return np.random.randint(low=0,high=len(self.rand_colors_dict),size=(self.tam_x,self.tam_y)).astype(int)
    
    def gen_poblacion_inicial(self):
        for i in range(self.poblacion):
            ind = self.gen_random_individuo()
            self.poblacion_actual.append({"individuo":ind,"fitness":self.fitness(ind)})
    
    def mostrar_individuo(self,individuo):
        ind = []
        for x in range(self.tam_x):
            ind.append([])
            for y in range(self.tam_y):
                ind[x].append(self.rand_colors_dict[individuo[x][y]])
        plt.imshow(ind)
        plt.show()
        
    def evaluar(self):
        if self.poblacion_elite[0]["fitness"] >= self.fitness_min:
            return True
        print("El mejor candidadto hasta ahora es {}".format(self.poblacion_elite[0]["fitness"]))
        return False

    def fitness(self,individuo):
        aptitud = 0
        cont_aptitud = 0
        for y in range(self.tam_y):
            for x in range(self.tam_x):
                norte = (x,y - 1) 
                oeste = (x - 1,y)
                sur = (x,y + 1)
                este = (x + 1,y)
                noroeste = (x - 1, y - 1)
                suroeste = (x - 1, y + 1)
                noreste = (x + 1, y - 1)
                sureste = (x + 1, y + 1)
                vecinos = [norte,sur,este,oeste,noreste,noroeste,sureste,suroeste]
                for vecino in vecinos:
                    xv,yv = vecino
                    if xv >=0 and yv >=0 and xv <= self.tam_x - 1 and yv <= self.tam_y - 1:
                        if(individuo[x][y] == individuo[xv][yv]):
                            aptitud = aptitud + 1
                        cont_aptitud = cont_aptitud + 1
        return aptitud/cont_aptitud

    def cruzar(self,individuo1,individuo2):
        for x in range(self.tam_y):
            for y in range(self.tam_x):
                if random.random() >= self.prob_cruza:
                    temp = individuo1["individuo"][x][y]
                    if not self.is_elite(individuo1):
                        individuo1["individuo"][x][y] = individuo2["individuo"][x][y]
                        individuo1["individuo"] = self.mutar(individuo1["individuo"])
                    if not self.is_elite(individuo2):
                        individuo2["individuo"][x][y] = temp
                        individuo2["individuo"] = self.mutar(individuo2["individuo"])
        self.calc_fitness(individuo1["individuo"])
        self.calc_fitness(individuo2["individuo"])


    def calc_fitness(self,individuo):
        self.poblacion_siguiente.append({"individuo":individuo,"fitness":self.fitness(individuo)})

    def mutar(self,individuo):
        for x in range(self.tam_y):
            for y in range(self.tam_x):
                if random.random() >= self.prob_mut:
                    individuo[x][y] = random.randint(0,len(self.rand_colors_dict))
        return individuo

    def elite(self):
        pob = sorted(self.poblacion_actual, key = lambda i: i['fitness'],reverse=True)
        num_pob_elite = int(self.poblacion * self.porcentaje_elite)
        self.poblacion_elite = pob[:num_pob_elite]
    
    def is_elite(self, individuo):
        for elite in self.poblacion_elite:
            if elite['fitness'] == individuo['fitness']:
                return True
        return False

    def evolucionar(self):
        self.gen_poblacion_inicial()
        self.elite()
        self.poblacion_siguiente = []
        for generacion in range(self.generaciones):
            if self.evaluar():
                print("Candidato adecuado encontrado")
                self.mostrar_individuo(self.poblacion_elite[0])
                break
            candidatos = []
            ind_num = 0
            for individuo in self.poblacion_actual:
                ind_num = ind_num + 1
                print("individuo {} de la generacion {}".format(ind_num,generacion))
                candidatos.append(individuo)
                if len(candidatos) == 2:
                    self.cruzar(candidatos[0],candidatos[1])
                    candidatos = []
            if len(candidatos) == 1:
                self.poblacion_siguiente.append(individuo)
            self.poblacion_actual = []
            self.poblacion_actual = self.poblacion_siguiente
            self.poblacion_siguiente = []
            self.elite()
        print("se llego al limite de generaciones")
        self.mostrar_individuo(self.poblacion_elite[0]["individuo"])


            
