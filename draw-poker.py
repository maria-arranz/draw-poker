
#librerías usadas

import random


#variables globales

values = ["A","K","Q","J","10","9","8","7","6","5","4","3","2"]
palo = ["♣","♦","♥","♠"]
manos = {1:"Royal flush",2:"Straight flush",3:"Quad",4:"Full House",5:"Flush",6:"Straight",7:"Set",8:"Pocket",9:"One pair",10:"High card"}

ranking = {"A":0,"2":12,"3":11,"4":10,"5":9,"6":8,"7":7,"8":6,"9":5,"10":4,"J":3,"Q":2,"K":1}

#función que construye el objeto baraja y lo "baraja"


def baraja():
    mi_baraja = [(x,y) for x in values for y in palo]
    random.shuffle(mi_baraja)
    return mi_baraja


#Criterios de seleccion de mano absolutos: color y escalera
#Funciones auxiliares: determinar si mismo color y si escalera


#Determina si todos los palos de una lista de palos son el mismo
def mismo_color(lista):
    palo = lista[0]
    if any(elem != palo for elem in lista): return False
    else:return True


#Auxiliar para poder ordenar las cartas
def mi_orden(elem):
    return ranking[elem[0]]

#Ordena una lista de cartas de mayor a menor valor
def ordena(lista):
    lista.sort(key=mi_orden)

#Comprueba si se tiene una escalera siendo A la carta más alta en una lista ordenada de cartas
def descendente(lista):
    count = ranking[lista[0]] - 1
    for elem in lista:
        if ranking[elem] != count + 1:
            return False
        else:
            count = ranking[elem]
    return True

#Comprueba si es el caso especial de una escalera donde A es la carta mas baja en una lista ordenada de cartas
def especial_flush(lista):
    return lista == ["A","5","4","3","2"]


#una mano será un set: esta funcion devuelve de cual se trata
def clasifica(mano):
    #como mano inmutable lo pasamos a lista
    s = list(mano)
    #a continuacion ordenamos la lista para tener una manera uniforme de detectar el tipo de mano
    ordena(s)
    valores = list(map(lambda x: x[0], s))
    palos = list(map(lambda x: x[1], s))
    color = mismo_color(palos)
    seguidas = descendente(valores)
    apariciones = list(map (lambda x: valores.count(x), values))
    maximo = max(apariciones)
    
    if (seguidas and color):
        if (valores[0] == "A"):
            return (1,"A")
        else:
            return (2,valores[0])
    
    if (color):
        if (especial_flush(valores)): return (2,"5")
        else: return (5,valores[0])
    if (maximo == 4):
        return (3,values[apariciones.index(4)])
    if(maximo == 3) and (2 in apariciones):
        return (4, values[apariciones.index(3)])
    if(seguidas):
        return (6, valores[0])
    if(especial_flush(valores)):
        return (6, "5")
    if(maximo == 3):
        return (7,values[apariciones.index(3)])
    if(apariciones.count(2) == 2):
        return (8,values[apariciones.index(2)]) #como estan ordenados, la primera aparicion tiene mayor valor
    if (2 in apariciones):
        return (9,values[apariciones.index(2)])
    else :return (10,valores[0])

# En conclusion se devuelve el tipo de mano y el primer criterio de desempate

# La parte del juego que implemento es el showdown: donde se decide que mano es la mejor

def showdown(valoraciones):
    indices = [i for i,elem in enumerate(valoraciones) if elem[0] == min(list(map(lambda x: x[0],valoraciones)))]
    #una vez tenemos los candidatos procedemos a intentar desempatar con el segundo argumento de salida de clasifica
    candidatos = [valoraciones[i] for i in indices]
    mejor = min(list(map(lambda x: ranking[x[1]],candidatos)))
    mejores = [indices[i] for i,elem in enumerate(candidatos) if ranking[elem[1]] == mejor]
    
    return mejores

#Aun así puede haber empate: hay que comparar el resto de las cartas
#posibilidades de empate en esta modalidad de poker (tener en cuenta que en otras modalidades puede ser necesario añadir mas casos):
# Flush, Pocket, One Pair, High Card
def desempate(j1,j2, mano):
    l1 = list(j1)
    l2 = list(j2)
    ordena(l1)
    ordena(l2)
    v1 = list(map(lambda x: x[0],l1))
    v2 = list(map(lambda x: x[0],l2))
    if(v1 == v2): return 0
    if (mano == 5 or mano == 10 or mano == 9): #en estos casos se mira cual es el que tiene la carta mas alta
        if any(v1[i] > v2[i] for i in range(5)): return -1
        else: return 1
    if (mano == 8): #en este caso en primer lugar se mira la segunda pareja y a continuacion, si es necesario la carta restante
        l1 = list(map (lambda x: valores.count(x), v1)).reverse
        l2 = list(map (lambda x: valores.count(x), v2)).reverse
        ind1 = 12 - l1.index(2)
        ind2 = 12 - l2.index(2)
        if (values[ind1] == values[ind2]):
            ind1 = 12 - l1.index(1)
            ind2 = 12 - l2.index(1)
        if(values[ind1] > values[ind2]):
            return -1
        else:
            return 1

#ESTO ESTA MAL -> FIJATE: que no has definido valores en ningun sition

def reparto(baraja, descarte,n):
    rep =[]
    for i in range(n):
        rep.append(set())
    for i in range(5):
        for j in range(n):
            if len(baraja) == 0:
                baraja = baraja + descarte
                random.shuffle(baraja)
                descarte.clear()
            rep[j].add(baraja[0])
            baraja.pop(0)
    return rep

def juego():
    mi_baraja = baraja()
    descarte = []
    n = int(input("jugadores:"))
    play = True
    while(play):
        rep = reparto(mi_baraja,descarte,n)
        print(to_string_reparto(rep))
        valoraciones = list(map(clasifica, rep))
        print(to_string_valoracion(valoraciones))
        mejor = showdown(valoraciones)
        aux = []
        while(len(mejor)> 1):
        ## solo es posible el empate entre un maximo de 4 jugadores con una sola baraja
        #iremos comparando los elementos con el primero de manera que podamos mantener control de los mejores
            factor = desempate(rep[mejor[0]], rep[mejor[1]],valoraciones[mejor[0]][0])
            if factor == 0:
                aux.append(mejor[1])
                mejor.remove(1)
            elif factor == -1:
                mejor.remove(1)
            else:
                aux.clear()
                mejor.remove(0)
        ganadores = mejor+aux
        print(to_string_ganador(ganadores))

        #REVISAR QUE SE HAGA BIEN, no me fio
        descarte = descarte + [x for lista in list(map(lambda x: list(x), rep)) for x in lista]
        a = (input("seguir (Y/N): "))
        if(a=="N"):
            play = False
        else: continue


def to_string_lista(lista):
    string = str(lista[0])
    for i in range(len(lista)-2):
        string = string +", " + str(lista[i+1])
    string = string + " y " + str(lista[len(lista)-1])
    return string

def to_string_ganador(ganadores):
    if len(ganadores) == 1:
        return "El ganador es el jugador: " + str(ganadores[0]+ 1) + ". Enhorabuena!"
    else: return "Ha habido un empate entre los jugadores "+ to_string_lista(ganadores)

def to_string_mano(conjunto):
    string = ""
    for elem in conjunto:
        string = string + "|" +elem[0]+ " " + elem[1] + "|"
    return string

def to_string_reparto(reparto):
    string = ""
    for i in range(len(reparto)):
        string = string + "Jugador " + str(i+1) + ":\n" + to_string_mano(reparto[i]) + "\n"
    return string

def to_string_valoracion(valoracion):
    string = ""
    for i in range(len(valoracion)):
        string = string + "Jugador " + str(i+1) + ": " + manos[valoracion[i][0]] + ", " + str(valoracion[i][1]) + "\n"
    return string

juego()
