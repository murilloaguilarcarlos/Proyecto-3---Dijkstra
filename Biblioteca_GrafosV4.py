"Carlos Murillo Aguilar"
import random
import math
"Clases y funciones"
class Nodo:
    def __init__(self, i):
        self.idn=i              # Crear objeto nodo, conformado solo por
                                #  su identificador numérico
class Arista:
    def __init__(self, a, b):
        self.arista=[Nodo(a),Nodo(b)]# Crear objeto arista, conformado por una 
                                     #  lista de dos nodos
def Color():    
    r = random.randrange(0, 254, 23)  # Función para generar colores aleatorios
    g = random.randrange(0, 254, 23)
    b = random.randrange(0, 254, 23)    
    return '"#{:02x}{:02x}{:02x}"'.format(r, g, b)

class Grafo:
    def __init__(self):            # Crear objeto grafo, conformado por una 
        self.nodos=[]              #  lista de los identificadores de cada nodo
        self.aristas=[]            #  y una lista de parejas de identificadores
                                   #  de cada nodo en cada arista
    def agregarNodo(self, n):
        if n not in self.nodos:
            nodo=Nodo(n)
            self.nodos.append(nodo.idn)
            
    def agregarArista(self, e1, e2):
        if e1 in self.nodos and e2 in self.nodos and [e1, e2] not in self.aristas and [e2, e1] not in self.aristas:
            aristaIds=Arista(e1, e2)
            self.aristas.append([aristaIds.arista[0].idn,  aristaIds.arista[1].idn])
            # self.aristas.append([aristaIds.arista[1].idn,  aristaIds.arista[0].idn])
    
    def generar_archivo(self, tipo_de_grafo, T, exp_aristas):         #Se define el nombre del archivo
        if tipo_de_grafo==1:
            s=open("Grafo de Malla.gv","w")
        elif tipo_de_grafo==2:
            s=open("Grafo de Erdös y Rényi.gv","w")
        elif tipo_de_grafo==3:
            s=open("Grafo de Gilbert.gv","w")
        elif tipo_de_grafo==4:
            s=open("Grafo Geográfico Simple.gv","w")
        elif tipo_de_grafo==5:
            s=open("Grafo Barabási-Albert.gv","w")
        elif tipo_de_grafo==6:
            s=open("Grafo Dorogovtsev-Mendes.gv","w")
        elif tipo_de_grafo==7:
            s=open("Grafo BFS.gv","w")
        elif tipo_de_grafo==8:
            s=open("Grafo DFS-R.gv","w")
        elif tipo_de_grafo==9:
            s=open("Grafo DFS-I.gv","w")
        elif tipo_de_grafo==10:
            s=open("Grafo Dijkstra.gv","w")
        
        s.write("digraph sample {\n")
        
        if tipo_de_grafo == 7:           # Para cada tipo de árbol se aplica un coloreado diferente
            for l in range(len(T)):
                c=Color()
                for n in T[l]:
                    w=(str(n) + " [color=" + str(c) + "];\n")
                    # print(w)
                    s.write(w)          # Para el árbol BFS se colorea cada capa y se eliminan
                                         #  las aristas que unan nodos de la misma capa
        if tipo_de_grafo == 8:
            c=[]
            b=[]
            self.color_R(T, c, b)
            print (c)                   # Para el árbol DFSR se coloréan las ramas n 
            print (b)                   #  dependiendo de que turno de elección fueron durante
            for bif in range(len(b)):   #  la búsqueda
                for r in b[bif]:
                    w=(str(r) + " [color=" + str(c[bif]) + "];\n")
                    s.write(w)
                    
        if tipo_de_grafo == 9:
            c=[]
            b=[]
            self.color_I(T, c, b)       # Para el árbol DFSI se colorean también las ramas,
            print (c)                   #  sin embargo, dado el algorítmo de búsqueda, 
            print (b)                   #  se colorean las ramas desde la bifurcación original
            col=[]                      #  hasta que una nueva se encuentre
            col_list=[]
            for bif in range(len(b)):
                w=(str(b[bif]) + " [color=" + str(c[bif]) + "];\n")
                s.write(w)
                col_list.append([b[bif], c[bif]])
            for n in range(len(T)):
                for bif in range(len(b)):
                    if T[n][0] == b[bif] and T[n][1] not in b:
                        w=(str(T[n][1]) + " [color=" + str(c[bif]) + "];\n")
                        s.write(w)
                        col_list.append([T[n][1], c[bif]])
                        
                    elif T[n][0] not in b and T[n][1] not in b \
                                          and T[n][1] not in col:
                        for clr in range(len(col_list)):
                            if T[n][0]==col_list[clr][0]:
                                w=(str(T[n][1]) + " [color=" + str(col_list[clr][1]) + "];\n")
                                s.write(w)
                                col.append(T[n][1])
                                col_list.append([T[n][1], col_list[clr][1]])
                
        if tipo_de_grafo == 10:
            print(T)
            for i in range(len(T)):
                r=T[i][0]
                r2=T[i][1]
                w=(str(r) + ' [label="'+ str(r) +'(' + str(r2) + ')"];\n')
                s.write(w)
            
        if tipo_de_grafo in range (7):
            print(self.aristas)
            for p in range(len(self.aristas)): # Escritura de cada arista para
                e1=str(self.aristas[p][0])     #   los generadores de grafos
                e2=str(self.aristas[p][1])
                flecha=" -> "
                puntocoma=';\n'
                w=e1+flecha+e2+puntocoma
                s.write(w)
                
        if tipo_de_grafo == 7:
            for p in range(len(self.aristas)):
                if self.aristas[p] in exp_aristas:
                    a=0
                    for l in range (len(T)):
                        if self.aristas[p][0] in T[l] and self.aristas[p][1] in T[l]:
                            a=1
                    if a==0:
                        e1=str(self.aristas[p][0])  # Para los árboles, se añade la etiqueta
                        e2=str(self.aristas[p][1])  #  que mantiene de color negro la arista
                        flecha=" -> "
                        puntocoma='[color="black"];\n'            
                        w=e1+flecha+e2+puntocoma
                        s.write(w)
            
        elif tipo_de_grafo >= 8:
            for p in range(len(self.aristas)):
                if self.aristas[p] in exp_aristas:
                    e1=str(self.aristas[p][0])
                    e2=str(self.aristas[p][1])
                    flecha=" -> "
                    puntocoma='[color="black"];\n'            
                    w=e1+flecha+e2+puntocoma
                    # print(w)
                    s.write(w)
            
        for i in range(len(self.nodos)):    # Se escribe cada nodo que no se encuentra en una arista
            b=False
            while b==False:
                for j in range(len(self.aristas)):
                    if self.nodos[i] in self.aristas[j]:
                        b=True
                if b==False:
                    # print(g.nodos[i])
                    ns=str(self.nodos[i])
                    w2=str(ns + puntocoma)
                    s.write(w2)
                b=True 
        
        s.write("}")        # Se finaliza y cierra el archivo del grafo
        s.close()
    
    def color_R(self, T, c, b):         # Función para determinar la cantidad de 
        for r in range(len(T)):         #  colores necesaria para el árbol DFSR
            if len(T) > len(c):
                c.append(Color())
                b.append([])
            if type(T[r]) is list:
                b[r].append(T[r][0])
                self.color_R(T[r], c, b)
        return c, b
    
    def color_I(self, T, c, b):         # Función para determinar la cantidad de
        # print (T)                     #  colores necesaria para el árbol DFSI
        c_exp_ar=[]
        for r in range(len(T)):
            for rr in range(len(T)):
                if T[rr][0] == T[r][0] and T[rr] != T[r] and T[r][0] not in b and T[rr] not in c_exp_ar:
                    b.append(T[r][0])
                    c_exp_ar.append(T[rr])
        for r in range(len(b)):
            c.append(Color())
        return c, b
    
    def BFS(self, s,T,exp,exp_aristas):
        T.append([s])
        exp.append(s)                             # Generación del árbol BFS
        i=0                                       #  El nodo fuente (s) se asigna a la lista de la 
        w=1                                       #  capa 0, mientras que todos los nodos de las 
        while w==1:                               #  áristas en las que participe el nodo s, quedan
            T.append([])                          #  registrados en la capa 1. Análogamente los nodos 
            for j in range(len(T[i])):            #  que toquen la capa anterior, se registran en una nueva capa
                for k in range (len(self.aristas)):
                    if T[i][j] in self.aristas[k] and self.aristas[k][0] not in exp and self.aristas[k][0] not in T[i+1]:
                        T[i+1].append(self.aristas[k][0])
                        exp.append(self.aristas[k][0])
                        exp_aristas.append(self.aristas[k])
                    if T[i][j] in self.aristas[k] and self.aristas[k][1] not in exp and self.aristas[k][1] not in T[i+1]:
                        T[i+1].append(self.aristas[k][1])
                        exp.append(self.aristas[k][1])
                        exp_aristas.append(self.aristas[k])
            if T[i+1]==[]:
                w=0
            i+=1
        print("Cantidad de capas: " + str(len(T)-1))
        return T
    
    def DFSR(self, s, T, exp, exp_aristas):                           # Generación del arbol DFS-Recursivo
        R=[s]                                                         #  El primer nodo que toque al nodo fuente 
        T.append(R)                                                   #  llamara nuevamente a esta misma función, 
        exp.append(s)                                                 #  pasando a convertirse en el nuevo nodo fuente.
        for a in range(len(self.aristas)):                            #  Así, se continua avanzando sobre una linea de
            if s in self.aristas[a] and self.aristas[a][0] not in exp:#  aristas, y cada vez que se termine una
                exp_aristas.append(self.aristas[a])                   #  trayectoria continua, la función terminará y 
                self.DFSR(self.aristas[a][0], R, exp, exp_aristas)    #  permitirá buscar trayectorias alternas al nodo 
            if s in self.aristas[a] and self.aristas[a][1] not in exp:#  en tuno.
                exp_aristas.append(self.aristas[a])
                self.DFSR(self.aristas[a][1], R, exp, exp_aristas)        
    
    def DFSI(self, s, T, exp, exp_aristas, stack):
        stack.append(s)    # Generación del árbol DFS-Iterativo:
        r=s                #  Iniciando desde el nodo fuente, se añadirá cada nodo explorado a una lista, de modo que al
        i=1                #  terminar una trayectoria, se irán eliminando los últimos elementos de dicha lista hasta
        while i==1:        #  encontrar una trayectoria alterna en alguno de los nodos. Las trayectorias ignorarán las
            # print(stack) #  aristas con nodos en la lista de pendientes.
            for a in range(len(self.aristas)):
                if r in self.aristas[a] and self.aristas[a] not in exp_aristas:
                    if (self.aristas[a][0] in stack and self.aristas[a][1] in stack)\
                        or (self.aristas[a][0] in exp) or (self.aristas[a][1] in exp):
                        True
                    else:
                        exp_aristas.append(self.aristas[a])
                        if self.aristas[a][1]==r and self.aristas[a][0] not in stack:
                            stack.append(self.aristas[a][0])
                        elif self.aristas[a][0]==r and self.aristas[a][1] not in stack:
                            stack.append(self.aristas[a][1])
                        a=0
                        r=stack[-1]
            exp.append(r)
            stack.remove(stack[-1])
            a=0            
            if len(stack)==0:
                i=0
            else:
                r=stack[-1]
        T.extend(exp_aristas)

    def Dijkstra(self, s,sum_values,exp,exp_aristas,values):
        print(self.aristas)
        for i in range (len(self.aristas)):
            values.append(random.randrange(1, 21))       
        print(values)
        mstvalue=0
        minimum=[]
        minimum_aristas=[]
        vet_aristas=[]
        exp_values=[]
        exp.append(s)
        a=1
        while a==1:
            # print(exp)
            for n in exp:
                for i in range(len(self.aristas)):
                    if n in self.aristas[i]\
                    and self.aristas[i] not in minimum_aristas\
                    and self.aristas[i] not in exp_aristas\
                    and self.aristas[i] not in vet_aristas\
                    and self.aristas[i][1] != n:
                        minimum_aristas.append(self.aristas[i])
                        minimum.append(values[i])
            # print(minimum_aristas)
            # print(minimum)
            if len(minimum) > 0:
                min_value = min(minimum)
                v0=minimum_aristas[minimum.index(min_value)][0]
                # print(v0)
                v1=minimum_aristas[minimum.index(min_value)][1]
                # print(v1)
                if v0 not in exp or v1 not in exp:
                    exp_aristas.append(minimum_aristas[minimum.index(min_value)])
                    exp_values.append(min_value)
                else:
                    vet_aristas.append(minimum_aristas[minimum.index(min_value)])
                if v0 not in exp and v1 in exp:
                    exp.append(v0)
                elif v1 not in exp and v0 in exp:
                    exp.append(v1)
            else:
                a=0
            minimum.clear()
            minimum_aristas.clear()
        print(exp_aristas)
        print(exp_values)
        sum_values.append([s,0])
        exp_sum=[]
        def suma(ind,n0,vi):
            for n in reversed(exp_aristas[:ind]):
                if n[1] == n0:
                    vi += exp_values[exp_aristas.index(n)]
                    # exp_sum.append(n)
                    suma(ind-1,n[0],vi)
            return vi
        for i in reversed(exp_aristas):
            ind=len(exp_aristas)
            vi=exp_values[exp_aristas.index(i)]
            distancia = suma(ind,i[0],vi)
            sum_values.append([i[1], distancia])
        # print(sum_values)

"Grafo de Malla"
def malla(i, j, dirigido=False): # i columnas, j filas
    g=Grafo()
    T=[]
    exp=[]
    exp_aristas=[]
    n=1
    m=[]
    for vi in range (i):
        r=[]
        for vj in range (j):
            r.append(n)
            g.agregarNodo(n)
            n+=1
        m.append(r)
    # print(m)
    
    for vi in range (i):
        for vj in range (j):            
            nij=m[vi][vj]            
            if vi<(i-1):
                g.agregarArista(nij, m[vi+1][vj])
            if vj<(j-1):
                g.agregarArista(nij, m[vi][vj+1])
    g.generar_archivo(1,T,exp_aristas)

"Grafo de Erdös y Rényi"
def eyR(n,a,dirigido=False): #n nodos, a aristas
    g=Grafo()
    r=[]
    aristas=[]
    T=[]
    exp=[]
    exp_aristas=[]
    for i in range (n):
        g.agregarNodo(i+1)
        r.append(i+1)    
    
    for i in range (a+1):
        # print (r)
        n1=random.choice(r)        
        n2=random.choice(r)
        if [n1, n2] not in aristas and [n2, n1] not in aristas and n1!=n2:
            g.agregarArista(n1, n2)
            aristas.append([n1, n2])
        else:
            i=i-1
    # print(aristas)
    g.generar_archivo(2,T,exp_aristas)
    
"Grafo de Gilbert"
def gilbert(n, p, dirigido=False):
    g=Grafo()
    r=[]
    aristas=[]
    T=[]
    exp=[]
    exp_aristas=[]
    for i in range (n):
        g.agregarNodo(i+1)
        r.append(i+1)    
    
    for i in r:
        for j in r:
            prob=random.random()
            if prob<=(p/200) and [i, j] not in aristas \
                             and [j, i] not in aristas and i!=j:
                g.agregarArista(i, j)
                aristas.append([i, j])
    # print(aristas)
    g.generar_archivo(3,T,exp_aristas)
    
"Grafo Geográfico Simple"
def simple(n, r, dirigido=False):
    g=Grafo()
    T=[]
    exp=[]
    exp_aristas=[]
    nodos=[]
    coords=[]
    aristas=[]
    box=n*4
    for i in range (n):
        g.agregarNodo(i+1)
        nodos.append(i+1)
        x=random.randrange(-box,box)
        y=random.randrange(-box,box)
        coords.append([x, y])
    print(coords)
    for i in (nodos):
        for j in (nodos):            
            pd=math.sqrt((coords[j-1][0]-coords[i-1][0])**2+(coords[j-1][1]-coords[i-1][1])**2)
            if pd<=r and [i, j] not in aristas and [j, i] not in aristas and i!=j:
                g.agregarArista(i, j)
                aristas.append([i, j])
    # print(aristas)
    g.generar_archivo(4,T,exp_aristas)
    
"Grafo Barabási-Albert"
def byA(n, a, dirigido=False):
    g=Grafo()
    T=[]
    exp=[]
    exp_aristas=[]
    nod_vert=[]
    nodos=[]
    aristas=[]
    phi=(1+math.sqrt(5))/2
    for i in range (n):
        g.agregarNodo(i+1)
        nodos.append(i+1)
        nod_vert.append(0)
        for j in range (len(nodos)):
            prob=random.random()
            if prob<=(1/(phi**(0.5*nod_vert[j]))) and nod_vert[j]<=a \
                                            and nod_vert[i]<=a \
                                            and [i, j] not in aristas \
                                            and [j, i] not in aristas and i!=j:
                g.agregarArista(i, j)
                aristas.append([i, j])
                nod_vert[j]+=1
                nod_vert[i]+=1
    # print(nod_vert)
    g.generar_archivo(5,T,exp_aristas)
    
"Grafo Dorogovtsev-Mendes"
def dyM(n, dirigido=False):
    g=Grafo()
    T=[]
    exp=[]
    exp_aristas=[]
    nodos=[1, 2, 3]
    for i in range(len(nodos)):
        g.agregarNodo(i+1)
    aristas=[[1,2], [2,3], [1,3]]
    for i in range(len(aristas)):
        g.agregarArista(aristas[i][0], aristas[i][1])    
    for i in range(4, n+1):        
        g.agregarNodo(i)
        nodos.append(i)
        a=random.choice(aristas)
        if [a[0], i] not in aristas and [i ,a[0]] not in aristas and \
           [a[1], i] not in aristas and [i ,a[1]] not in aristas and \
           i!=a[0] and i!=a[1]:
            g.agregarArista(a[0], i)
            g.agregarArista(a[1], i)
            aristas.append([a[0], i])
            aristas.append([a[1], i])
    g.generar_archivo(6,T,exp_aristas)

"Grafos de búsqueda"
def search(tipo):
    s=open("grafo.gv","r")
    lectura=[]
    aristas=[]
    g=Grafo()
    rL=s.readlines()
    for i in range(1, len(rL)-1):
        if "->" in rL[i]:
            lectura.append(rL[i][0:-2])        
            aristas.append(lectura[i-1].split(" -> "))
            e1=int(aristas[i-1][0])
            e2=int(aristas[i-1][1])
            aristas[i-1][0]=e1
            aristas[i-1][1]=e2
            g.agregarNodo(e1)
            g.agregarNodo(e2)
            g.agregarArista(e1, e2)
        else:
            lectura.append(rL[i][0:-2])
            aristas.append(lectura[i-1])
            e1=int(aristas[i-1])
            g.agregarNodo(e1)
    g.nodos.sort()
    
    s=int(input("-Elegir nodo fuente-\nNodos disponibles: "+str(g.nodos[0])+"-"+str(g.nodos[-1])+"\n--> "))
    T=[]
    exp=[]
    exp_aristas=[]
    stack=[]
    values=[]
    sum_values=[]
    if tipo=="BFS":
        g.BFS(s,T,exp,exp_aristas)
        tipo_de_grafo=7
    elif tipo=="DFSR":
        g.DFSR(s,T,exp,exp_aristas)
        tipo_de_grafo=8
    elif tipo=="DFSI":
        g.DFSI(s,T,exp,exp_aristas,stack)
        tipo_de_grafo=9
    elif tipo=="Dijkstra":
        g.Dijkstra(s,sum_values,exp,exp_aristas,values)
        tipo_de_grafo=10
    # print(T)
    # print(exp_aristas)
    if tipo=="Dijkstra":
        g.generar_archivo(tipo_de_grafo, sum_values, exp_aristas)
    else:
        g.generar_archivo(tipo_de_grafo, T, exp_aristas)
    

# malla(5,6) # (5,6):30, (10,10):100, (20,25):500  columnas, filas
# eyR(30,29) # nodos, aristas
# gilbert(127,15) # nodos, porcentaje de probabilidad
# simple(500,309) # nodos, radio
# byA(30,5) #nodos, aristas máximas por nodo
# dyM(500) #nodos
BFS="BFS"    # Selección del tipo de árbol de búsqueda
DFSR="DFSR"
DFSI="DFSI"
Dijkstra="Dijkstra"
search(Dijkstra)