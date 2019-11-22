# Algoritmo genetico con colores
## algoritmo
### Crear poblacion aleatoria
### Evaluar población
### Repetir hasta lograr objetivo o llegar a M generaciones
* Seleccion de individuos % elitista, ruleta o torneo
* Cruza de individuos (2 intercambian atributos) - salen 2 hijos; Generar aleatorio(A<Pc) si es menor entonces no se cruza sale igual
* Mutación indivual de nuevos individuos; Generar aleatorio si (T<Pm) si sale igual no muta
* Evaluar a la nueva población
### Parametros iniciales
* M generaciones
* N individuos
* PC probabilidad de cruza <= .85
* PM Probabilidad de mutacion <=.2
* elitismo %10