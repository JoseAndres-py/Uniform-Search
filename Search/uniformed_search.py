import util
import search
import pygame


class graph_problem(search.SearchProblem):
    def __init__(self, vertices, edges,start,goal):
        self.G = {v:{} for v in vertices}
        for v1, v2, c in edges:
            if (self.G[v2] != {v1:c}):
                self.G[v1][v2] = c
            #(self.G[v2])[v1] = c
        self.start = vertices[start]
        self.goal = vertices[-goal]

    def getStartState(self):
        return self.start

    def isGoalState(self, state):
        return self.goal == state

    def getSuccessors(self, state):
        suc = self.G[state]
        successors = [(suc, str(state),
                       (self.G[state])[suc]) for suc in self.G[state]]
        return successors

def general_ui_search(problem, frontier,Display):
    visited = {}
    state = problem.getStartState()
    frontier.push((state, [], 0))
    visited[state] =(255,153,153)   #Pink
    while not frontier.isEmpty():
        u, actions, path_cost = frontier.pop()
        #print(u)
        if problem.isGoalState(u):
            return  actions,visited, path_cost
        #print(u,actions)
        #print(problem.getSuccessors(0))

        for v, action, cost in problem.getSuccessors(u):
            a = frontier.count(v)

            if (not v in visited) and not len(a):
                frontier.push((v, actions + [action],path_cost + cost))
                pygame.draw.rect(Display,(153,255,255),[int(v%30)*20+1,int(v/30)*20+1,20-1,20-1],0)
        #print ("\nExpanding parent node "+str(u))
        #print ("Fringe: "+ str([frontier.__dict__['list'][x][0] for x in range(len(frontier.__dict__['list']))]))


        visited[u] = (153,153,255) #Lila
        # Avanzamos y actualizamos la pantalla con lo que hemos dibujado.
        pygame.display.flip()

        #time.sleep(0.03)
    return [],[],[]


def general_search(problem, frontier, Display):
    visited = {}
    state = problem.getStartState()
    frontier.push((state, [], 0))
    while not frontier.isEmpty():
        u, actions, path_cost = frontier.pop()
        if problem.isGoalState(u):
            return  actions, visited, path_cost
        if not u in visited:
            for v, action, cost in problem.getSuccessors(u):
                frontier.push((v, actions + [action], path_cost + cost))
                pygame.draw.rect(Display, (153, 255, 255), [int(v % 30) * 20 + 1, int(v / 30) * 20 + 1, 20 - 1, 20 - 1],0)
            #print ("\nExpanding parent node "+str(u))
            #print ("Fringe: "+ str([frontier.__dict__['heap'][x][2][0] for x in range(len(frontier.__dict__['heap']))]))


        visited[u] = 'Cyan'
    return [], [],[]


def dfs(problem,DYSP):
   return general_ui_search(problem, util.Stack(),DYSP)

def bfs(problem,DYSP):
   return general_ui_search(problem, util.Queue(),DYSP)

def uniformCostSearch(problem,DYSP):
    def g_cost(item):
        return item[2]
    return general_search(problem, util.PriorityQueueWithFunction(g_cost),DYSP)

def search_Tree(Obs = [],ObsCost = [],Longitud = 0):
    #Arbol de problemas
    Leng_Mat = Longitud
    edges = []
    vertices = range(Longitud**2)

    #Movimientos
    Left = -1; Rigth = 1; Down = 1; Up = -1

    #Posibles Rutas
    for col,obstaculo in enumerate(Obs):
        for fil,Value in enumerate(obstaculo):
            #print('Pos = ',fil,col)
            if not(Obs[col][fil]):
                Id = fil+col*Leng_Mat
                #print('Id = ',Id)

                if (col > 0) and (Obs[col+Up][fil] != 1):
                    Id_son = fil+(col+Up)*Leng_Mat
                    #print('Movimiento Arriba:',Id,Id_son)
                    edges.append((Id,Id_son,ObsCost[col+Up][fil]))
                if (col < Leng_Mat-1) and (Obs[col+Down][fil] != 1):
                    Id_son = fil+(col+Down)*Leng_Mat
                    #print('Movimiento Abajo:',Id,Id_son)
                    edges.append((Id,Id_son,ObsCost[col+Down][fil]))

                if (fil > 0) and (Obs[col][fil+Left] != 1):
                    Id_son = fil+Left+col*Leng_Mat
                    #print('Movimiento Izquierda:',Id,Id_son)
                    edges.append((Id,Id_son,ObsCost[col][fil+Left]))
                if (fil < Leng_Mat-1) and (Obs[col][fil+Rigth] != 1):
                    Id_son = fil+Rigth+col*Leng_Mat
                    #print('Movimiento Derecha:',Id,Id_son)
                    edges.append((Id,Id_son,ObsCost[col][fil+Rigth]))

    return edges,vertices
