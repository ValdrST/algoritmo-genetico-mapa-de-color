from Genetica import Genetica
import numpy as np
import random
import matplotlib.pyplot as plt
import threading
import math

class Color_map(Genetica):
    def __init__(self,prob_cruza=0.7,prob_mut=0.3,porcentaje_elite=0.1,poblacion=1000,generaciones=100, fitness_min = 0.9,tam_x=8,tam_y=8):
        Genetica.__init__(self,prob_cruza,prob_mut,porcentaje_elite,poblacion,generaciones,fitness_min)
        self.tam_x = tam_x
        self.tam_y = tam_y
        self.rand_colors_dict = [(0,0,255),(255,255,0),(0,255,0),(255,0,0)]
        self.disp_color = [17,18,13,16]
    @staticmethod
    def gen_random_color():
        return (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    
    
    def gen_random_individuo(self):
        disp_color = []
        for disp in self.disp_color:
            disp_color.append(disp)
        ind = np.zeros((self.tam_x*self.tam_y))
        for i in range(self.tam_x*self.tam_y):
            color_rand = random.randint(0,len(self.rand_colors_dict)-1)
            while disp_color[color_rand] == 0:
                color_rand = random.randint(0,len(self.rand_colors_dict)-1)
            disp_color[color_rand] = disp_color[color_rand] - 1
            ind[i] = color_rand
        return ind.reshape(self.tam_x,self.tam_y)
            

        return np.random.randint(low=0,high=len(self.rand_colors_dict),size=(self.tam_x,self.tam_y)).astype(int)
    
    def add_random_individuo(self):
        ind = self.gen_random_individuo()
        self.poblacion_actual.append({"individuo":ind,"fitness":self.fitness(ind)})

    def gen_poblacion_inicial(self):
        for i in range(self.poblacion):
            threading.Thread(target=self.add_random_individuo).start()
        while len(self.poblacion_actual) < self.poblacion:
            pass
    
    def contar_colores(self,individuo):
        color = np.zeros((len(self.rand_colors_dict)))
        for col in individuo.reshape(self.tam_x*self.tam_y):
            color[int(col)] = color[int(col)] + 1
        return color


    def mostrar_individuo(self,individuo):
        ind = []
        for x in range(self.tam_x):
            ind.append([])
            for y in range(self.tam_y):
                ind[x].append(self.rand_colors_dict[int(individuo[x][y])])
        plt.imshow(ind)
        print(self.poblacion_actual)
        print(self.contar_colores(individuo))
        plt.show()
        
    def evaluar(self):
        if self.poblacion_elite[0]["fitness"] >= self.fitness_min:
            return True
        return False

    @staticmethod
    def fit_opt(individuo,tam_x,tam_y):
        aptitud = 0
        cont_aptitud = 0
        for y in range(tam_y):
            for x in range(tam_x):
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
                    if xv >=0 and yv >=0 and xv <= tam_x - 1 and yv <= tam_y - 1:
                        if(individuo[x][y] == individuo[xv][yv]):
                            aptitud = aptitud + 1
                        cont_aptitud = cont_aptitud + 1
        return aptitud/cont_aptitud
    
    @staticmethod
    def fit_opt_2(individuo,tam_x,tam_y):
        aptitud = 0
        cont_aptitud = 0
        for y in range(tam_y):
            for x in range(tam_x):
                val_act = individuo[x][y]
                for y2 in range(tam_y):
                    for x2 in range(tam_x):
                        if x != x2 or y != y2:
                            if val_act == individuo[x2][y2]:
                                aptitud = aptitud + math.sqrt((x2-x)**2+(y2-y)**2)
                                cont_aptitud = cont_aptitud + 1
        return (aptitud/cont_aptitud)/10

    def fitness(self,individuo):
        ##return self.fit_opt_2(individuo,self.tam_x,self.tam_y)
        return self.fit_opt(individuo,self.tam_x,self.tam_y)
        

    def cruzar(self,individuo1,individuo2):
        temp = individuo1["individuo"]
        for x in range(self.tam_y):
            for y in range(self.tam_x):
                if not self.is_elite(individuo1):
                    if random.random() <= self.prob_cruza:
                        individuo1["individuo"][x][y] = individuo2["individuo"][x][y]
                if not self.is_elite(individuo2):
                    if random.random() <= self.prob_cruza:
                        individuo2["individuo"][x][y] = temp[x][y]
        individuo1 = self.mutar(individuo1)
        individuo2 = self.mutar(individuo2)
        self.calc_fitness(individuo1["individuo"])
        self.calc_fitness(individuo2["individuo"])

    def gen_rand_pos(self):
        x = random.randint(0,self.tam_x-1)
        y = random.randint(0,self.tam_y-1)
        return x,y

    def calc_fitness(self,individuo):
        self.poblacion_siguiente.append({"individuo":individuo,"fitness":self.fitness(individuo)})

    def mutar(self,individuo):
        ind = individuo
        individuo = individuo["individuo"]
        if not self.is_elite(ind):
            for x in range(self.tam_y):
                for y in range(self.tam_x):
                    if random.random() <= self.prob_mut:
                        rand_x = random.randint(0,self.tam_x-1)
                        rand_y = random.randint(0,self.tam_y-1)
                        temp = individuo[x][y]
                        individuo[x][y] = individuo[rand_x][rand_y]
                        individuo[rand_x][rand_y] = temp
        ind["inidividuo"] = individuo
        return ind

    def elite(self):
        pob = sorted(self.poblacion_actual, key = lambda i: i['fitness'],reverse=True)
        num_pob_elite = int(self.poblacion * self.porcentaje_elite)
        self.poblacion_elite = pob[:num_pob_elite]

    def is_elite(self, individuo):
        for elite in self.poblacion_elite:
            if elite['fitness'] == individuo['fitness']:
                return True
        return False
    
    def sust_not_elite(self,poblacion):
        poblacion_nueva = []
        for pob in poblacion:
            if self.is_elite(pob):
                poblacion_nueva.append(pob)
            else:
                ind = self.gen_random_individuo()
                poblacion_nueva.append({"individuo":ind,"fitness":self.fitness(ind)})
        return poblacion_nueva


    def evolucionar(self):
        self.gen_poblacion_inicial()
        self.elite()
        self.poblacion_siguiente = []
        for generacion in range(self.generaciones):
            if self.evaluar():
                print("Candidato adecuado encontrado")
                self.mostrar_individuo(self.poblacion_elite[0]["individuo"])
                break
            else:
                print("generacion {} El mejor candidato hasta ahora es {}".format(generacion+1,self.poblacion_elite[0]["fitness"]))
            candidatos = []
            ind_num = 0
            while len(self.poblacion_actual) > 0:
                ind_num = ind_num + 1
                candidatos.append(self.poblacion_actual.pop())
                if len(candidatos) == 2:
                    threading.Thread(target=self.cruzar,args=(candidatos[0],candidatos[1],)).start()
                    candidatos = []
            if len(candidatos) == 1:
                poblacion_siguiente.append(candidatos.pop())
            while(len(self.poblacion_siguiente)<self.poblacion):
                pass
            self.poblacion_actual = []
            self.poblacion_actual = self.sust_not_elite(self.poblacion_siguiente)
            self.poblacion_siguiente = []
            self.elite()
        self.mostrar_individuo(self.poblacion_elite[0]["individuo"])


            
