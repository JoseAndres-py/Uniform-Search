import numpy as np
import pygame
import uniformed_search as us
import sys
from time import time

#################################################################
##                           FUNCIONES                         ##
#################################################################

def ObtenerMatriz(Nombre = 'null'):

    with open(Nombre, 'r') as file:
        lineas = [linea.split(',') for linea in file.readlines()]
        #print(lineas[0])
        for idx,fila in enumerate(lineas):
            col = len(fila)-1
            lineas[idx][col] = fila[col].replace('\n','')
        lineas = [list(map(int,i)) for i in lineas]
        return lineas
def Dibujar_Laberinto(Obstaculos, Display, Start = [0,0],Goal = [1,1]):
    Tamano_Cuadro = 20
    # Limpiar la consola
    Display.fill(Negro)

    # range(inicia, fin, de a cuanto)
    for i in range(1, Dimensiones[0],Tamano_Cuadro):
        for j in range(1,Dimensiones[1],Tamano_Cuadro):
            #Normalizar
            x=int(i/Tamano_Cuadro)
            y=int(j/Tamano_Cuadro)
            if Obstaculos[y][x] == 0:
                # pygame.draw.rect(Donde se dibuja, color, area(x,y,largo,ancho), groso borde )
                pygame.draw.rect(Display,Blanco,[i,j,Tamano_Cuadro-1,Tamano_Cuadro-1],0)
    Start = Start*Tamano_Cuadro+1
    Goal = Goal*Tamano_Cuadro+1
    # Start, Goal
    pygame.draw.rect(Display,Rojo,[Start[0],Start[1],Tamano_Cuadro-1,Tamano_Cuadro-1],0)
    pygame.draw.rect(Display,Verde,[Goal[0],Goal[1],Tamano_Cuadro-1,Tamano_Cuadro-1],0)


#################################################################
##                           ALGORITMO                         ##
#################################################################

#print("Argumentos",sys.argv)
if len(sys.argv) != 1:
    Algoritmo_Busqueda = sys.argv[1]

else:
    Algoritmo_Busqueda = 'dfs'

pygame.init()

#Colores
Blanco = (255,255,255)
Negro = (0,0,0)
Verde = (0,255,0)
Rojo = (255,0,0)

Laberinto = ObtenerMatriz("./maze.txt")
Costos = ObtenerMatriz("./maze_cost.txt")

#Pantalla
Dimensiones = [600,600]
Pantalla = pygame.display.set_mode(Dimensiones)
pygame.display.set_caption("Algoritmos Jose y Andrea")


#El bucle se ejecuta hasta que el usuario hace click sobre el boton de cierre.
Cerrar = False
#Se usa para establecer cuan rapido se actualiza la pantalla
reloj = pygame.time.Clock()

Dibujar_Laberinto(Obstaculos=Laberinto,Display=Pantalla,Start = np.array([1,0]), Goal = np.array([29,28]))
edges1,vertices1 = us.search_Tree(Laberinto,Costos,30)
problem1 = us.graph_problem(vertices1, edges1,1,31)
#Eleccion Algoritmo

start_time = time()

if Algoritmo_Busqueda == 'bfs':
    actions, visitados, costo= us.bfs(problem1,Pantalla)
elif Algoritmo_Busqueda == 'dfs':
    actions, visitados, costo = us.dfs(problem1, Pantalla)
elif Algoritmo_Busqueda == 'ucs':
     actions, visitados, costo= us.uniformCostSearch(problem1,Pantalla)

# Calculate the elapsed time.
elapsed_time = time() - start_time

print "Path to goal found: "
print ('Accciones = ', actions)
print ('# Accciones = ', len(actions))
print ('# Visitados = ', len(visitados))
print ('Costo = ',costo)
print("Elapsed time: %0.10f seconds." % elapsed_time)


#Dibujar Ruta Optima
for Id in actions:
    pygame.draw.rect(Pantalla,(153,153,255) ,[int(Id)%30*20+1,int(Id)/30*20+1,20-1,20-1],0)

while not Cerrar:
    #Bucle eventos
    for Evento in pygame.event.get():
        if Evento.type == pygame.QUIT:
            Cerrar= True
    # Avanzamos y actualizamos la pantalla con lo que hemos dibujado.
    pygame.display.flip()
    # Limitamos a 60 fotogramas por segundo (frames per second)
    reloj.tick(60)

pygame.quit()
