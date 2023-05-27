import sys
from constraint import *
import random

#Esta función se utiliza para ordenar el diccionario que contiene una solución
def ordenar(solucion):
    #Se crea el diccionario que estará ordenado
    ordenado = dict()
    #Se crea un valor para el que cualquier asiento sea un número menor que este
    valor = 33
    #Aquí se almacenará la variable correspondiente al valor que se tiene en el momento como primero
    var = str()
    #Se lleva un registro de las variables que faltan por visitar
    var_restantes = list()

    #Se añaden todas las variables a la lista de variables restantes
    for x in variables:
        var_restantes.append(x)

    #Se hacen tantas iteraciones como número de elementos
    for i in range(len(solucion)):
        #Se comparan todas las variables que aún no se han ordenado
        for x in range(len(var_restantes)):
            #Si el asiento de una variable es menor que el valor registrado, se actualiza el valor y la
            #variable correspondiente
            if solucion[var_restantes[x]] < valor:
                var = var_restantes[x]
                valor = solucion[var_restantes[x]]
        #Se elimina la variable resultante de la lista de restantes
        var_restantes.remove(var)
        #Se añade la variable y su posición en el nuevo diccionario
        ordenado[var] = valor
        #se vuelven a inicializar las variables para la siguiente iteración
        valor = 33
        var = str()
    #Se devuelve la solución ordenada
    return ordenado

#se abre el fichero que se ha pasado para hacer la ejecución
f = open(sys.argv[1],'r')
#En cada línea existe un alumno, por lo que se crea una lista con las líneas
lineas = f.readlines()
f.close()
#Se crea la línea en la que se van a almacenar los alumnos
alumnos = list()
#Para cada línea leida
for x in lineas:
    #se separan los datos
    linea = x.split(",")
    #Se guarda cada dato correspondiente con el tipo de dato que es
    id = int(linea[0])
    ciclo = int(linea[1])
    conflictivo = linea[2]
    movilidad = linea[3]
    hermano = int(linea[4])
    #Se crea una tupla con todos los campos
    tupla = (id,ciclo,conflictivo,movilidad,hermano)
    #Se añade el alumno a la lista de alumnos
    alumnos.append(tupla)

#Se crea la clase encargada de resolver el problema
problem = Problem()
#Se crea una lista que almacenará todas las variables
variables = list()
#Para cada alumno
for x in range(len(alumnos)):
    #Se crea la variable correspondiente
    var = str(alumnos[x][0])+alumnos[x][2]+alumnos[x][3]
    #se añade a las variables
    variables.append(var)

    #Si el alumno no tiene movilidad reducida
    if alumnos[x][3] == 'X':
        #Si es del ciclo 1 y no tiene hermanos, o su hermano también es del ciclo 1
        if alumnos[x][1] == 1 and (alumnos[x][4] == 0 or alumnos[(alumnos[x][4])-1][1] == 1):
            problem.addVariable(var,[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])

        # Si es del ciclo 2 y no tiene hermanos, o su hermano también es del ciclo 2
        elif alumnos[x][1] == 2 and (alumnos[x][4] == 0 or alumnos[(alumnos[x][4])-1][1] == 2):
            problem.addVariable(var,[17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32])

        #Llegados a este punto los hermonos no son del mismo ciclo
        # Si el hermano tiene movilidad reducida
        elif alumnos[(alumnos[x][4])-1][3] == 'R':
            # el alumno actual se debe sentar en la sección 1
            problem.addVariable(var, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
        # Si x es el mayor
        elif alumnos[x][1] == 2:
            #Debe estar en el pasillo de la seccion 1
            problem.addVariable(var, [2,3,6,7,10,11,14,15])
        #Si es el menor
        else:
            #Tiene que estar sentado en una ventana de la seccion 1
            problem.addVariable(var, [1, 4, 5, 8, 9, 12, 13, 16])


    # Si el alumno tiene movilidad reducida
    elif alumnos[x][3] == 'R':
        # Si es del ciclo 1 y no tiene hermanos, o su hermano también es del ciclo 1
        if alumnos[x][1] == 1 and (alumnos[x][4] == 0 or alumnos[(alumnos[x][4])-1][1] == 1):
            problem.addVariable(var,[1,2,3,4,13,14,15,16])
        # Si es del ciclo 2 y no tiene hermanos, o su hermano también es del ciclo 2
        elif alumnos[x][1] == 2 and (alumnos[x][4] == 0 or alumnos[(alumnos[x][4])-1][1] == 2):
            problem.addVariable(var,[17,18,19,20])
        # Si tiene hermanos y no coincide el ciclo se debe sentar en la seccion 1, pero en asientos reservados
        else:
            problem.addVariable(var,[1,2,3,4,13,14,15,16])

#No puede asignarse el mismo asiento a dos alumnos
problem.addConstraint(AllDifferentConstraint(),variables)

#Si x tiene movilidad reducida
def mov_reducida(x,i):
    #Si el asiento es par, no puede estar nadie en el de su izquierda
    if x%2 == 0:
        if i != x-1:
            return True
        else:
            return False
    # Si el asiento es impar, no puede estar nadie en el de su derecha
    else:
        if i != x+1:
            return True
        else:
            return False

#Si x es un alumno conflictivo
def alumno_conflictivo(x,i):
    restr_cumplida = False
    #Si esta en alguna esquina, no puede sentarse en los 3 asientos adyacentes
    if x == 1:
        if i not in [2,5,6]:
            restr_cumplida = True
    elif x == 4:
        if i not in [3,7,8]:
            restr_cumplida = True
    elif x == 29:
        if i not in [25,26,30]:
            restr_cumplida = True
    elif x == 32:
        if i not in [25,26,30]:
            restr_cumplida = True
    #Si se sienta en los pasillos exteriores, existen 5 asientos adyacentes
    elif (x -1 ) % 4 == 0:
        if i != x-4 and i != x-3 and i != x+1 and i != x+4 and i != x+5:
            restr_cumplida = True
    elif (x - 4) % 4 == 0:
        if i != x-4 and i != x-5 and i != x-1 and i != x+3 and i != x+4:
            restr_cumplida = True
    #Si se sienta en la primera fila, hay 5 asientos adyacentes
    elif x in [2,3]:
        if i != x-1 and i != x+3 and i != x+4 and i != x+5 and i != x+1:
            restr_cumplida = True
    #Si se sienta en la ultima fila, hay 5 asientos adyacentes
    elif x in [30,31]:
        if i != x-1 and i != x-5 and i != x-4 and i != x-3 and i != x+1:
            restr_cumplida = True
    #Si esta en un asiento diferente a los mencionados anteriormente, existen 8 asientos adyacentes
    else:
        if i != x-5 and i != x-4 and i != x-3 and i != x-1 and i != x+1 and i != x+3 and i != x+4 and i != x+5:
            restr_cumplida = True
    return restr_cumplida

#si x y h son hermanos
def sentar_hermanos(x,h):
    #Si x esta en un asiento par, h esta en el de su izquierda
    if x%2 == 0 and h == x-1:
        return True
    # Si x esta en un asiento impar, h está en el de su derecha
    elif x%2 != 0 and h == x+1:
        return True
    #Si esta distinto de lo anterior, no están juntos
    else:
        return False

#Si alguno de los hermanos tiene movilidad reducida
def sentar_hermanos_mov_reducida(x,h):
    #Si esto ocurre, solo hace falta que se encuentren en la misma sección, y las dos existentes son:
    seccion_1 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    seccion_2 = [17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]
    #Si x está en una, h tiene que estar en la misma
    if x in seccion_1 and h in seccion_1:
        return True
    elif x in seccion_2 and h in seccion_2:
        return True
    #si no están en la misma se devuelve False
    else:
        return False

#Para cada alumno existente
for x in range(len(alumnos)):
    #Si tiene movilidad reducida
    if alumnos[x][3] == 'R':
        #Para el resto de los alumnos
        for i in range(len(alumnos)):
            if i != x:
                #Se verifica que nadie esté sentado a su lado
                problem.addConstraint(mov_reducida,(variables[x],variables[i]))

    #Si es un alumno problemático
    if alumnos[x][2] == 'C':
        #Para el resto de alumnos
        for i in range(len(alumnos)):
            #Si el alumno es conflictivo o tiene movilidad reducida
            #Esto no aplica si un alumno es su hermano
            if i != x and alumnos[x][4] != i+1 and (alumnos[i][2] == 'C' or alumnos[i][3] == 'R'):
                #Se verifica que no haya ninguno sentado cerca suyo
                problem.addConstraint(alumno_conflictivo, (variables[x], variables[i]))

    #Si tiene algún hermano
    if alumnos[x][4] != 0:
        #Se saca el hermano
        hermano = alumnos[x][4]-1
        #Si alguno de los dos tiene movilidad reducida
        if alumnos[hermano][3] == 'R' or alumnos[x][3] == 'R':
            #En este caso no hace falta que estén al lado, pero sí en la misma sección
            problem.addConstraint(sentar_hermanos_mov_reducida, (variables[x], variables[hermano]))
        #Si ninguno tiene movilidad reducida
        else:
            #Deben estar sentados al lado
            problem.addConstraint(sentar_hermanos,(variables[x],variables[hermano]))

#Se generan las soluciones del problema
soluciones = problem.getSolutions()

# Se abre el fichero en el que hay que escribir el resultado
with open((sys.argv[1] + '.output'), 'w') as f:
    # Se escribe el número de soluciones
    f.write("Numero de soluciones: "+str(len(soluciones))+"\n")
    # Se seleccionan 3 de estas soluciones, o todas si el número es menor de 3
    # se controla con el contador i
    i = 0
    while i < min(3, len(soluciones)):
        # Se genera un número aleatorio entre el número de soluciones
        aleatorio = random.randint(0, len(soluciones))
        # Se ordena la solución de la posición generada
        definitivo = ordenar(soluciones[aleatorio])
        # Se escibe la solución
        f.write(str(definitivo)+"\n")
        # Se suma 1 al contador
        i += 1
