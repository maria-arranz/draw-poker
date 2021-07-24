
#librerías usadas

import random


#variables globales

values = ["A","K","Q","J","10","9","8","7","6","5","4","3","2"]
palo = ["♣","♦","♥","♠"]
manos = {1:"Royal flush",2:"Straight flush",3:"Quad",4:"Full House",5:"Flush",6:"Straight",7:"Set",8:"Pocket",9:"One pair",10:"High card"}


#función que construye el objeto baraja y lo "baraja"

def baraja():
    mi_baraja = [(x,y) for x in values for y in palo]
    random.shuffle(mi_baraja)
    return mi_baraja
    
#check    
print(baraja())
