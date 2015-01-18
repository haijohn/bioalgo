# -*- coding: utf-8 -*-

"""

Unit6: Looking for Fragile Regions in the Human Genome

"""

def position(k, P):
    """ find the position in P, when the element in P equals either k or -k
    :param k: integer
    :param P: a tuple contains integers
    >>> position(1, (1,2,3))
    0
    >>> position(1, (-1,2,3))
    0
    """
    try:
        return P.index(k)
    except ValueError:
        try :
            return P.index(-k)
        except ValueError as e:
            print "Error: %s"%e

def is_sorted(i, P):
    return P[i-1] == i

def k_sorting_reversal(k, P):
    """ assume prefix k-1 element is is_sorted, put the kth element in place by reversal
    >>> k_sorting_reversal(2, (1,3,2))
    (1, -2, -3)
    >>> k_sorting_reversal(2, (1,3,4,2))
    (1, -2, -4, -3)
    """   
    #print k
    pos = position(k, P)
    dest_pos = k-1
    lp = list(P) 
    total_index = pos + dest_pos
    total_range = pos - dest_pos

    print total_index
    print total_range
    #assert pos > dest_pos
    if total_range % 2 == 0:
        half_range = total_range / 2
        #print half_range
        for i in range(dest_pos, dest_pos+half_range):
            #print i,total_range-i
            lp[i], lp[total_index-i] = -lp[total_index-i], -lp[i]
        lp[dest_pos+half_range] = -lp[dest_pos+half_range]
    else:
        half_range = (total_range + 1) / 2
        #print half_range
        for i in range(dest_pos, dest_pos+half_range):
            #print i,total_range-i
            lp[i], lp[total_index-i] = -lp[total_index-i], -lp[i]        
    return tuple(lp)

def flip_k(k, P):
    lp = list(P)
    lp[k-1] = -lp[k-1]
    return tuple(lp)

def greedy_sorting(P):
    """Input: A permutation P.
       Output: The sequence of permutations corresponding to applying GREEDYSORTING to P, 
               ending with the identity permutation.
    >>> greedy_sorting((-3,4,1,5,-2))
    [(-1, -4, 3, 5, -2),
     (1, -4, 3, 5, -2),
     (1, 2, -5, -3, 4),
     (1, 2, 3, 5, 4),
     (1, 2, 3, -4, -5),
     (1, 2, 3, 4, -5),
     (1, 2, 3, 4, 5)]
    """
    l = len(P)
    permutations = []
    for i in range(1, l+1):
        if P[i-1] != i and P[i-1] != -i:
            P = k_sorting_reversal(i, P)
            permutations.append(P)
        if P[i-1] == -i:
            P = flip_k(i, P)
            permutations.append(P)
    return permutations

def parse_text(t):
    return tuple(int(i) for i in t[1:-1].split(' '))

def output_text(t):
    return '('+' '.join(['+'+str(i) if i>0 else str(i) for i in t]) + ')'
