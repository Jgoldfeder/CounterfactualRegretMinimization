# Written By Judah Goldfeder

# A few utility functions that will be shared by both the seqential and normal form Kunh Poker implementations
import random
import numpy as np
# returns a card tuple for players 1 and 2
def get_cards():
    cards = [1,2,3]
    card_1 = random.choice(cards)
    cards.remove(card_1)
    card_2 = random.choice(cards)
    return card_1, card_2
    
    
def normalize(array):
    # copy array so as not to destroy items
    arr2 = []
    for i in array:
        arr2.append(i)
    array = arr2
    # ignore negative regrets
    sum = 0
    for i in array:
        if i>0:
            sum += i
    for idx, val in enumerate(array):
        if sum == 0:
            array[idx] = 1/len(array) # uniform
        else:
            array[idx] = max(0,val/sum)
    return np.array(array)        
