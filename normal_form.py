# Written By Judah Goldfeder

import random, sys
from util import normalize, get_cards


    
# player 1 has 3 info states, one for each possible card observed   
# they then have the following actions for each info-state
# 0) bet
# 1) pass and then bet
# 2) pass and then pass


# p2 also has 3 info states, one for each possible card observed
# they then have the following actions for each info-state

# 0) always pass
# 1) if p1 pass, pass. if p1 bet, bet
# 2) if p1 pass, bet.  if p1 bet, pass
# 3) always bet

def get_random_strategy(player):
    if player == 1:
        # 3 actions for each info state
        num_actions = 3
    else:
        # 4 actions for each info state
        num_actions = 4
        
    strategy = {}
    for info_state in range(1,4):    
        actions = []
        for i in range(num_actions):
            actions.append(random.uniform(0, 1))
        actions = normalize(actions)
        strategy[info_state] = actions
    
    return strategy

    
def get_utility(p1_action, p2_action, c1, c2):
    
    if    ((p1_action == 0 and p2_action == 1) 
        or (p1_action == 0 and p2_action == 3) 
        or (p1_action == 1 and p2_action == 2)
        or (p1_action == 1 and p2_action == 3)):

        # betting stand off:
        if c1>c2:
            return 2, -2
        else:
            return -2, 2
    
    if ((p1_action == 1 and p2_action == 0) 
     or (p1_action == 1 and p2_action == 1)
     or (p1_action == 2 and p2_action == 0) 
     or (p1_action == 2 and p2_action == 1)):
        # passing stand off
        if c1>c2:
            return 1, -1
        else:
            return -1, 1    
    
    if p1_action == 0:
        return 1, -1
    if p1_action == 2:       
        return -1, 1

def get_action(info_state,strategy):
    strategy = strategy[info_state]
    num = random.uniform(0, 1)
    prob_mass = 0
    for idx, val in enumerate(strategy):
        prob_mass += val
        if prob_mass > num:
            return idx
    return len(strategy) - 1

    
def minimize_reget(iter):
    p1_strategy = get_random_strategy(player=1)
    p2_strategy = get_random_strategy(player=2)
    
    p1_s_sum = {1 : [0,0,0], 2 : [0,0,0], 3: [0,0,0]}
    p2_s_sum = {1 : [0,0,0,0], 2 : [0,0,0,0], 3: [0,0,0,0]}

    p1_r_sum = {1 : [0,0,0], 2 : [0,0,0], 3: [0,0,0]}
    p2_r_sum = {1 : [0,0,0,0], 2 : [0,0,0,0], 3: [0,0,0,0]}
        
    for i in range(iter):
        c1,c2 = get_cards()
        a1 = get_action(c1, p1_strategy)
        a2 = get_action(c2, p2_strategy)
        
        r = get_utility(a1, a2, c1, c2)
        
        for a in range(3):
            p1_r_sum[c1][a] += get_utility(a, a2, c1, c2)[0] - r[0]
        p1_strategy[c1] = normalize(p1_r_sum[c1])
        #if(c1==1):
            #print(p1_regret,a1,a2)
        for a in range(4):
            p2_r_sum[c2][a] += get_utility(a1, a, c1, c2)[1] - r[1]    
        p2_strategy[c2] = normalize(p2_r_sum[c2])

        for idx,val in enumerate(p1_strategy[c1]):
            p1_s_sum[c1][idx] += val
        for idx,val in enumerate(p2_strategy[c2]):
            p2_s_sum[c2][idx] += val    
    
    
    for info_state in range(1,4):
        p1_s_sum[info_state] = normalize(p1_s_sum[info_state])
        p2_s_sum[info_state] = normalize(p2_s_sum[info_state])

    return p1_s_sum, p2_s_sum

def get_expected_value(p1_strategy, p2_strategy):
    value = 0
    for c1 in [1,2,3]:
        for c2 in [1,2,3]:
            if c1==c2:
                continue
            for a1 in range(3):
                for a2 in range(4):
                    utility = get_utility(a1,a2,c1,c2)
                    prob = (1/6) * p1_strategy[c1][a1] * p2_strategy[c2][a2]
                    value += utility[0]*prob
    return value
  
if __name__ == "__main__":  
    p1_strategy, p2_strategy = minimize_reget(int(sys.argv[1]))    
    print(get_expected_value(p1_strategy,p2_strategy))   
