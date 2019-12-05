# Algoritmo genetico con colores
## algoritmo
### Crear poblacion aleatoria
### Evaluar población
### Repetir hasta lograr objetivo o llegar a M generaciones
* Seleccion de individuos % elitista, ruleta o torneo
* Cruza de individuos (2 intercambian atributos) - salen 2 hijos; Generar aleatorio(A<Pc) si es menor entonces no se cruza sale igual
* Mutación indivual de nuevos individuos; Generar aleatorio si (T<Pm) si sale igual no muta
* Evaluar a la nueva población

## Detalles tecnicos de la implementacion
### Parametros recibidos
* probabilidad de cruza [0 - 1.0]
* probabilidad de mutacion [0 - 1.0] 
* porcentaje de poblacion elite [0 - 1.0] 
* poblacion [1 - N]
* Numero de generaciones [1 - N]
* finess minimo [0 - 1.0]

### generacion de la poblacion inicial
* Recibir numero de colores que se van a tener (genes)
* Recibir la disposicion de los genes ejemplo: [17 rojos, 18, amarillos, 13 verdes, 19 azules]
* Poblar vector de forma aleatoria con los genes
* Convertir vector a matriz de NxN

### Calcular elite
* Ordenar individuos por su valor de fitness
* añadir a poblacion elite el numero de individuos definidio por poblacion elite
  - si es una poblacion de 100 y la poblacion elite es de 10% entonces se tomaran los 10 mejores (10 primeros de la poblacion ordenada)

### evaluar generacion
* tomar el mejor de la poblacion elite
  - Si el mejor esta en dentro del fitness minimo se detiene el algoritmo

### Cruzar individuos
* Si se toma de forma secuencial 2 individuos
* para cada individuo
  - Si el individuo esta dentro de la poblacion elite entonces este pasa sin modificacion
  - Si no esta entonces se calcula la probabilidad de cruza
  - Si se cruza entonces se calcula una posicion aleatoria de sustitucion. Ejemplo ind1 [1,2,2,2,3] ind2 [2,2,2,1,3] pos_random = 2 ind2[:2] = [1,3]. ind1_new = [1,2,2,1,3].

### Mutar individuo
* si el individuo esta dentro de la poblacion elite este no se muta
* Si se va a mutar entonces se procesa gen por gen la probabilidad de mutacion y si esta sale positiva entonces se intercambia un gen por otro del mismo elemento.
  - ejemplo ind = [1,2,2,1,1] mutacion_ind = [2,1,2,1,1], en este ejemplo se muto la posicion 0 y se intercambio por la 1. 

### Calcular fitness de individuo
* Se calculan las posiciones de los genes adjuntos
  - norte,sur,este,oeste,suroeste,noroeste,sureste,noreste.
* por cada gen se compara en todas las direcciones posibles, si el gen de x posicion es igual al gen del centro entonces se aumenta un contador de genes iguales
 ![ejemplo grafico](algoritmo_color/img/img_1.png?raw=false "Busqueda de patrones")
  - Si es igual o no se tiene otro contador que aumenta para contar el numero de comparaciones hechas
* Se obtiene el promedio de todas las comparaciones hechas en cada gen y este debe dar un valor comprendido entre [0 - 1.0] donde 1.0 es 100%.


### Algoritmo evolucionar
1. generar poblacion inicial
2. calcular elite de la poblacion inicial
3. evaluar generacion actual
4. cruzar individuos
5. mutar individuos
6. sustuir poblacion inicial con poblacion siguiente
7. repetir desde el punto 2. hasta que no se cumpla la condicion de fitness minimo o el numero de generaciones definido
8. mostrar mejor individuo 
