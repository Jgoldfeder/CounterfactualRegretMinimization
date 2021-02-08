# Written By Judah Goldfeder

import random, sys
from collections import defaultdict
import numpy as np
import util
from util import normalize, get_cards

PASS = 0
BET = 1
action_to_string = ["p","b"]


# get the utility, given a history and a set of cards    
# returns a tuple in the form (p1_util, p2_util)
def utility(h,cards):
    if h[-1] == "p" and h[-2] == "p":
        if cards[0] > cards[1]:
            return 1,-1
        return -1,1
    if h[-1] == "b" and h[-2] == "b":
        if cards[0] > cards[1]:
            return 2,-2
        return -2,2
    if h[-1] == "p" and h[-2] == "b": 
        if(len(h)==3):
            return -1,1   
        return 1,-1
    if h[-1] == "b" and h[-2] == "p":        
        return -1,1    

# history is stored as a string of "h" and "b"   
def is_terminal(h):
    if len(h) == 3:
        return True
    if len(h) <= 1:
        return False
    if h[-1] == "p" and h[-2] == "p":
        return True
    if h[-1] == "b" and h[-2] == "b":
        return True    
    if h[-1] == "p" and h[-2] == "b":
        return True 
    return False
   
def cfr(h,player_to_update,pi_1,pi_2,cards,strategy,strategy_sum,regret_sum):
    # all this ugly modulus math calculates the player and opponent from the history length
    player = ((len(h)) % 2)+1
    opponent = ((len(h)+1) % 2)+1

    if is_terminal(h):
        u= utility(h,cards)[player-1]
        return u
        
    # info set is simply the history concatenated with the card that the current player sees    
    info_set = str(cards[player-1]) + h

    # in the main part of the CFR algorithm, we recursivly call CFR, passing in the probabilities of our current strategy
    # we also calculate the expected value of the info state given this strategy
    action_value = np.zeros(2)
    value = 0
    for action in [PASS,BET]:
        if player == 1:
            action_value[action] = -1 * cfr(h+action_to_string[action],player_to_update,pi_1*strategy[info_set][action],pi_2,cards,strategy,strategy_sum,regret_sum )
        elif player == 2:
            action_value[action] = -1 * cfr(h+action_to_string[action],player_to_update,pi_1,pi_2*strategy[info_set][action],cards,strategy,strategy_sum,regret_sum)
        value += action_value[action] * strategy[info_set][action]
    
    # in this implementation, we only update one player at a time
    if player == player_to_update:
        # calculate the regrets and update the strategy and regret sums
        probs = np.array([pi_1,pi_2])
        for action in [PASS,BET]:
            regret_sum[info_set][action] += probs[opponent-1] * (action_value[action] - value)
            strategy_sum[info_set][action] += probs[player-1] * strategy[info_set][action]
        # update the strategy
        strategy[info_set] = normalize( regret_sum[info_set])
    return value

# this function calculates the expected value of a strategy profile, given a set of cards    
def expected_value(h,p,cards,strategy,exp):
    opponent = ((len(h)+1) % 2)+1
    player = ((len(h)) % 2)+1

    info_set = str(cards[player-1]) + h
    if is_terminal(h):
        exp[info_set] = p * utility(h,cards)[0] #pi_1*pi_2 #utility(h,cards)[0]*probs[player-1]
        return 
    for action in [PASS,BET]:
        expected_value(h+action_to_string[action],p*strategy[info_set][action],cards,strategy,exp)

# util function to print out a strategy profile        
def print_strategy(str):
    print("*************************")
    keys = sorted(str.keys())
    for k in keys:
        print(k,str[k])
    print("*************************")


if __name__ == "__main__":
    num_iter = int(sys.argv[1])  

    strategy = defaultdict(lambda: np.array([0.5,0.5]))   
    strategy_sum = defaultdict(lambda: np.zeros(2))   
    regret_sum = defaultdict(lambda: np.zeros(2))

    for iter in range(num_iter):
        for i in [1,2]:
            cfr("",i,1,1,get_cards(),strategy,strategy_sum,regret_sum)
            
            
    normalized_strategy = {}        
    for k,v in strategy_sum.items():
        normalized_strategy[k] = normalize(v)
     


    # calculate expected value
    exp = 0
    for c1 in [1,2,3]:
        for c2 in [1,2,3]:
            if c1==c2:
                continue
            exp_dict = {}
            expected_value("",1/6,[c1,c2],normalized_strategy,exp_dict)
            for k,v in exp_dict.items():
               exp+=v 
    print(exp)









