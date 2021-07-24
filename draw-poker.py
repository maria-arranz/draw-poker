
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
