import numpy as np

class Genetica():
    def __init__(self,prob_cruza,prob_mut,porcentaje_elite=0.1,poblacion=100,generaciones=100, fitness_min = 0.9):
        self.prob_mut = prob_mut
        self.prob_cruza = prob_cruza
        self.porcentaje_elite = porcentaje_elite
        self.poblacion = poblacion
        self.generaciones = generaciones
        self.fitness_min = fitness_min
        self.aptitudes = []
        self.poblacion_elite = []
        self.poblacion_actual = []
        self.poblacion_siguiente = []
    

    def fitness(self):
        raise NotImplementedError

    def evaluar(self):
        raise NotImplementedError
    
    def cruzar(self):
        raise NotImplementedError

    def mutar(self):
        raise NotImplementedError

    def elite(self):
        raise NotImplementedError