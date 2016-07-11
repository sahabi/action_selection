import operator

def init_probs(P):
    num_states = len(P)
    for key in P:
        P[key] = 1./num_states
    return P

def det_k(P,prev_state,action):
    kl = 1
    kh = 2
    
    if action == 'east':
        for key in P:
            if key[0] <= prev_state[0]:
                P[key] = kl
            if key[0] > prev_state[0]:
                P[key] = kh
    if action == 'west':
        for key in P:
            if key[0] < prev_state[0]:
                P[key] = kh
            if key[0] >= prev_state[0]:
                P[key] = kl
    if action == 'north':
        for key in P:
            if key[1] < prev_state[1]:
                P[key] = kh
            if key[0] >= prev_state[0]:
                P[key] = kl
    if action == 'south':
        for key in P:
            if key[1] <= prev_state[1]:
                P[key] = kl
            if key[1] < prev_state[1]:
                P[key] = kh
    return P

def update_P(P,K):
    norm = 0
    for key in P:
        norm += P[key]*K[key]
    for key in P:
        P[key] = K[key]*P[key]/float(norm)
    return P

def get_max(P):
    maximum =  max(P.iteritems(), key=operator.itemgetter(1))[1]
    max_s = []
    for key in P:
        if P[key] == maximum:
            max_s.append(key)
    return max_s

def get_min_states(P):
    maximum =  min(P.iteritems(), key=operator.itemgetter(1))[1]
    min_s = []
    for key in P:
        if P[key] == maximum:
            min_s.append(key)
    if len(min_s) == 1:
        return min_s
    else:
        return min_s[0]

def manhattan_dist(s,st):
    return abs(s[0] - st[0]) + abs(s[1] - st[1])

def get_target(s,s_max):
    state_dict = {}
    for state in s_max:
        if state != s:
            state_dict[state] = manhattan_dist(s,state)
    return get_min_states(state_dict)

def move(s,a):
    if a == 'east':
        return (s[0]+1,s[1])
    if a == 'north':
        return (s[0],s[1]-1)
    if a == 'west':
        return (s[0]-1,s[1])
    if a == 'south':
        return (s[0],s[1]+1)
        
def get_s_h_l(current_s, action, S_max):
    
    s_h = {}
    s_h[(current_s,action)] = []
    s_l = {}
    s_l[(current_s,action)] = []
    for state in S_max:
        if manhattan_dist(move(current_s,action),state) <= manhattan_dist(current_s,state):
            s_h[(current_s,action)].append(state)
        if manhattan_dist(move(current_s,action),state) > manhattan_dist(current_s,state):
            s_l[(current_s,action)].append(state)
    return(s_h,s_l)

def get_delta_action(current_s, S_max, actions):
    delta_action_dict = {}
    
    for action in actions:
        (s_h,s_l) = get_s_h_l(current_s, S_max, action)
        s_h_num = len(s_h[(current_s,action)])
        s_l_num = len(s_l[(current_s,action)])
        delta_action = abs(s_h_num - s_l_num)
        delta_action_dict[action] = delta_action
        
    return delta_action_dict
    
def pick_action(delta_action_dict, current_state, target_state):
    actions = get_max(delta_action_dict)
    if len(actions) == 1:
        return actions[0]
    if len(actions) > 1:
        for action in actions:
            if manhattan_dist(move(current_state,action),target_state) < manhattan_dist(current_state,target_state):
                return action


P = {(0,0):0,(0,1):0,(0,2):0,(0,3):0,(1,0):0,(1,1):0,(1,2):0,(1,3):0,(2,0):0,(2,1):0,(2,2):0,(2,3):0,(3,0):0,(3,1):0,(3,2):0,(3,3):0}
P = init_probs(P)
K = det_k(P,(0,3),'east')
P = update_P(P,K)
S = get_max(P)
T = get_target((2,0),S)
print T