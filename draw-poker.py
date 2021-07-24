
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
