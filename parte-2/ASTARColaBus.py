import sys
import time

# Se crea la clase de cada nodo
class Estado:
    #Se define el init
    def __init__(self, estado, restantes, heuristica, alumnos):
        # Se define el estado como la lista de los alumnos que hay en la cola
        self.estado = estado
        # Se deben tener en cuenta los alumnos que faltan por añadir a la cola
        self.restantes = restantes
        #Se crea la variable que contiene los asientos asignados
        self.alumnos = alumnos
        # Se calcula el valor de la funcion g()
        self.g = self.coste_estado()
        # Dependiendo de la heurística seleccionada
        if heuristica == "1":
            self.h = self.heuristica_1()
        elif heuristica == "2":
            self.h = self.heuristica_2()
        # Si se ha introducido una heurística no válida, sa error
        else:
            raise Exception("Formato de heurística no válido")
        self.f = self.g + self.h

    # Se calcula el coste del estado
    def coste_estado(self):
        # Se crea una lista del coste resultante para cada alumno
        costes = list()
        # Con esta variable se define si la anterior es de movilidad reducida
        ayudar = False
        # Para cada alumno se calcula su tiempo
        for x in range(len(self.estado)):
            # Se añade la posicion a la lista
            costes.append(0)
            # Si no tiene que ayudar a alguien de movilidad reducida, tarda 1
            if not ayudar:
                costes[x] = 1
            # Si tiene movilidad reducida tarda 3
            if self.estado[x][2] == 'R':
                ayudar = True
                costes[x] = 3
            # Si tiene que ayudar, no tarda mas ya que va con la persona a la que ayuda
            else:
                ayudar = False

        # Se modifican los tiempos en funcion de los alumnos conflictivos
        for x in range(len(self.estado)):
            # Si es conflictivo
            if self.estado[x][1] == 'C':
                # Se duplica el tiempo de los que tiene al lado
                if x != 0:
                    costes[x-1] *= 2
                if x < len(self.estado)-1:
                    costes[x+1] *= 2
                # Para el resto de alumnos
                for i in range(len(self.estado)):
                    # Si los alumnos estan en la cola despues del conflictivo que se esta evaluando
                    # y se sienta en un asiento posterior que el conflictivo
                    if alumnos[self.estado[x]] < alumnos[self.estado[i]] and x < i:
                        # Se duplica su tiempo
                        costes[i] *= 2
        # Se suman todos los costes
        coste = sum(costes)
        return coste

    # Se define la primera heuristica
    def heuristica_1(self):
        coste_h = 0
        # Para los que quedan por añadir
        for x in self.restantes:
            # Si tiene movilidad reducida se estima un tiempo de 2
            if x[2] == 'R':
                coste_h += 2
            # Si no tiene movilidad reducida se estima un tiempo de 1
            else:
                coste_h += 1
        # Si la ultima posicion de los asignados es alguien con movilidad reducida
        if len(self.estado) > 1 and self.estado[-1][2] == 'R':
            # Se devuelve el total menos 1
            return coste_h-1
        else:
            # se devuelve el coste calculado
            return coste_h

    # Se define la segunda heurística
    def heuristica_2(self):
        # Si la ultima posicion de los asignados es alguien con movilidad reducida
        if len(self.estado) > 1 and self.estado[-1][2] == 'R':
            # Se estima que una persona de lso restantes no cuenta
            coste_h = len(self.restantes)-1
        else:
            # Se estima que se tarda 1 por cada persona
            coste_h = len(self.restantes)

        # Para cada persona que falta
        for x in restantes:
            # Si tiene movilidad reducida se estima una persona menos
            if x[2] == 'R':
                coste_h -= 1
        # Se devuelve el coste
        return coste_h


    #se comprueba si el estado es terminal
    def terminal(self):
        # Si no falta ninguna persona por añadir
        if len(self.restantes) == 0:
            # Se comprueba que tiene un formato valido
            if self.valido():
                return True
        return False

    # Se devuelve si el estado es valido
    def valido(self):
        # Para cada alumno en la cola
        for x in range(len(self.estado)):
            # Si es el ultimo de la cola y tiene movilidad reducida no es valido
            if x + 1 == len(self.estado) and self.estado[x][2] == 'R':
                return False
            # si tiene movilidad reducida y el siguiente tambien, no es valido
            elif x + 1 != len(self.estado):
                if self.estado[x][2] == 'R' and self.estado[x + 1][2] == 'R':
                    return False
        return True

# Se define la clase del arbol de busqueda
class Arbol:
    # Se definen sus  variables
    def __init__(self,estado_inical,alumnos):
        #El estado inicial
        self.inicial = estado_inical
        #Los asientos asignados
        self.alumnos = alumnos

    # se define el algoritmo de buscar la solucion
    def busqueda_ASTAR(self):
        # Se empieza a contar el tiempo de busqueda
        inicio = time.time()
        # Se crea la lista abierta
        lista_abierta = list()
        # Se añade el estado inicial
        lista_abierta.append(self.inicial)
        # Se añade un contador para contar los nodos expandidos
        numero_nodos = 0
        while True:
            # Se saca el primero de la lista
            actual = lista_abierta[0]
            lista_abierta.remove(actual)
            # se actualiza el contador
            numero_nodos += 1

            # Si es terminal
            if actual.terminal():
                # Se toma el tiempo
                final = time.time()
                # se calcula lo que se ha tardado
                tiempo = int(round((final - inicio),0))
                # Se devuelven los parámetros necesarios
                return actual.estado, tiempo, actual.g, len(actual.estado), numero_nodos
            # Si no es terminal
            else:
                # Se hace una lista de nodos a expandir
                expandidos = list()
                # Para persona de las que falta por añadir
                for x in actual.restantes:
                    # Se hacen dos nuevas listas, que seran las del nuevo estado
                    nuevos_restantes = list()
                    nuevo_estado = list()
                    # Se copian las listas anteriores a las nuevas
                    for j in actual.restantes:
                        nuevos_restantes.append(j)
                    for j in actual.estado:
                        nuevo_estado.append(j)
                    # Se elimina la persona que se añade de los restantes
                    nuevos_restantes.remove(x)
                    # se añade la persona a la lista de la cola
                    nuevo_estado.append(x)
                    # Se genera el nuevo estado y se introduce en la lista de expandidos
                    expandidos.append(Estado(nuevo_estado, nuevos_restantes, sel_heuristica, self.alumnos))

                # Se crea una lista para ordenar por coste los nodos
                ordenados = list()
                # Para cada expandido
                for x in expandidos:
                    # si no hay nada en la lista abierta se introduce el nodo
                    if len(lista_abierta) == 0:
                        ordenados.append(x)
                    # Si hay algo ya introducido
                    else:
                        # La posicion por defecto es la primera para introducir los estados
                        posicion = 0
                        # Se recorre la lista
                        for l in ordenados:
                            # Si la funcion f es mayor que la de el estado que ya esta en la lista
                            # Se avanza la posicion
                            if x.f > l.f:
                                posicion += 1
                        # se inserta en la posicion correspondiente
                        ordenados.insert(posicion, x)

                # Se crean variables para controlar la posicion de recorrer las listas
                posicion_expandidos = 0
                posicion_lista_abierta = 0
                # Mientras la posicion de los nuevos nodos no haya pasado la longitud de la lista
                while posicion_expandidos < len(ordenados):

                    # Si ya se ha llegado al final de la lista abierta
                    if posicion_lista_abierta >= len(lista_abierta):
                        # Se añade el nodo expandido al final de la lista abierta
                        lista_abierta.append(ordenados[posicion_expandidos])
                        # Se pasa al siguiente nodo expandido
                        posicion_expandidos += 1

                    # Si la funcion del nodo expandido es menor que la del nodo de la lista abierta
                    elif ordenados[posicion_expandidos].f < lista_abierta[posicion_lista_abierta].f:
                        # Se añade el nodo expandido antes del nodo de la lista abierta
                        lista_abierta.insert(posicion_lista_abierta,ordenados[posicion_expandidos])
                        # se pasa al siguiente nodo expandido
                        posicion_expandidos += 1

                    # Si el coste de f(x) es mayor o igual al del nodo de la lista abierta
                    else:
                        # Se pasa al siguiente nodo de la lista abierta
                        posicion_lista_abierta += 1

# Se abre el fichero que se ha pasado para hacer la ejecución
f = open(sys.argv[1],'r')
# Se crea un diccionario para los alumnos
alumnos = dict()
# Se lee el fichero
archivo = f.read()[1:-1]
# Se cierra el fichero
f.close()
# Se dividen los datos de cada alumno
datos = archivo.split(',')
# Se identifica si es el primer elemento
primer_elem = True
for x in datos:
    # Se dividen los datos en el alumno y el asiento
    dato = x.split(':')
    # Si es el primer alumno, no tiene un espacio al inicio de su nombre
    if primer_elem:
        alumnos[dato[0][1:-1]] = int(dato[1])
        primer_elem = False
    # Para el resto de alumnos
    else:
        alumnos[dato[0][2:-1]] = int(dato[1])
# Se recoge la heuristica indicada en uan variable
sel_heuristica = sys.argv[2]

# Se crean las listas para el estado inicial
estado_alumnos = list()
restantes = list()
# se llena la lista de restantes
for x in alumnos:
    restantes.append(x)

# Se crea el estado inicial
inicial = Estado(estado_alumnos,restantes,sel_heuristica,alumnos)
# Se crea el arbol de busqueda
Arbol_busqueda = Arbol(inicial, alumnos)
# Se llama a la funcion que busca la solucion
solucion,tiempo,coste,longitud,nodos_expandidos = Arbol_busqueda.busqueda_ASTAR()

# Se crea un diccionario que contiene los alumnos y su asiento en el orden de la solucion obtenida
final = dict()
for x in solucion:
    final[x] = alumnos[x]

# Se coge el nombre del fichero dado inicialmente
fichero = sys.argv[1].replace(".prob","")
# Se abre el fichero .output
f = open(fichero + "-" + sel_heuristica + ".output",'w')
# Se escriben las lineas correspondientes
f.write("INICIAL:  " + str(alumnos)+"\n")
f.write("FINAL:    " + str(final))
# Se cierra el fichero
f.close()

# Se abre el fichero .stat
f = open(fichero + "-" + sel_heuristica + ".stat",'w')
# Se escriben las lineas correspondientes
f.write("Tiempo total: " + str(tiempo) + "\n")
f.write("Coste total: " + str(coste) + "\n")
f.write("Longitud del plan: " + str(longitud) + "\n")
f.write("Nodos expandidos: " + str(nodos_expandidos))
# Se cierra el fichero
f.close()
