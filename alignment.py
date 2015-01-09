# -*- coding: utf-8 -*-

"""

Unit5: How Do We Compare Sequence ?

"""

def tower_of_hanoi(n, src, dest):
    if n == 1:
        print 'move from %s to %s'%(src, dest)
        return 
    transit = 6 - src - dest
    tower_of_hanoi(n-1, src, transit)
    print 'move from %s to %s'%(src, dest)
    tower_of_hanoi(n-1, transit, dest)
    return

## begin change money problem
def greedy_change(money, coins):
    """ use big coins first
    >>> greedy_change(18, [5,2,1])
    >>> [5,5,5,2,1] # corret solution
    >>> greedy_change(72, [14,12,1,3])
    >>> [14, 14, 14, 14, 14, 1, 1] # incorret solution
    """
    coins.sort(reverse=True)
    changes = []
    while money != 0:
        coin = coins[0]
        money -= coin
        if money < 0:
            money += coin
            coins.pop(0)
        else:
            changes.append(coin)
    return changes


def memoize(f):
    """top-down dynamic programming using memoize
       to avoid recaculation
    """
    cache = {}
    def wrapper(*args, **kwargs):
        key = args[0]
        if key in cache:
            val = cache[key]
        else:
            cache[key] = f(*args, **kwargs)
            val = cache[key]
        return val
    return wrapper

@memoize
def recussive_change(money, coins):
    """ brute force recussive search of all spaces
    """    
    if money == 0:
        return 0
    min_num_coins = money
    for coin in coins:
        if money >= coin:
            num_coin = recussive_change(money-coin, coins)
            if num_coin + 1 < min_num_coins:
                min_num_coins = num_coin + 1
    return min_num_coins


def dp_change(money, coins):
    min_num_coins = {}
    min_num_coins[0] = 0
    for m in range(1,money+1):
        min_num_coins[m] = money
        for coin in coins:
            if m >= coin:
                if min_num_coins[m-coin] + 1 < min_num_coins[m]:
                    min_num_coins[m] = min_num_coins[m-coin] + 1
    return min_num_coins[money]

# end change money problem

# begin Manhattan tourist problem
def build_matrix(matrix_str):
    """build a score matrix, down_matrix stores score of all vertical edge,
       right_matrix stores score of all horizontal edge"""
    return [[int(i) for i in line.split(' ')] for line in matrix_str.split('\n') if line]

def manhatten_tourist(n, m, down_matrix, right_matrix):
    """ use botton-up dynamic programming solve manhatten tourist problem"""
    s = {}
    s[(0,0)] = 0
    for i in range(1, n+1):
        s[(i,0)] = s[(i-1,0)] + down_matrix[i-1][0]
    for j in range(1, m+1):
        s[(0,j)] = s[(0,j-1)] + right_matrix[0][j-1]
    for i in range(1, n+1):
        for j in range(1, m+1):
            s[(i,j)] = max(
                            s[(i-1,j)] + down_matrix[i-1][j],
                            s[(i,j-1)] + right_matrix[i][j-1]
                           )
    return s[n,m]
# end Manhattan tourist problem


def toplogical_ordering(graph):
    ordering = []
    candidates = [node for node in graph.get_nodes() 
                          if graph.indegree(node) == 0]
    while candidates:
        candidate = candidates.pop()
        ordering.append(candidate)
        for edge in graph.out_edges(candidate):
            graph.remove_edge(edge)
        graph.remove_node(candidate)
        candidates = [node for node in graph.get_nodes() 
                          if graph.indegree(node) == 0]
    return ordering


# begin longest common substring problem
def lcs_backtrack(v, w):
    n,m = len(v),len(w)
    backtrack = {}
    s = {}
    s[(0,0)] = 0
    for i in range(1, n+1):
        s[(i,0)] = 0
    for j in range(1, m+1):
        s[(0,j)] = 0
    for i in range(1, n+1):
        for j in range(1, m+1):
            if v[i-1] == w[j-1]:
                s[(i,j)] = max(
                            s[(i-1,j)],
                            s[(i,j-1)],
                            s[(i-1,j-1)] + 1
                           )
            else:
                s[(i,j)] = max(
                            s[(i-1,j)],
                            s[(i,j-1)],
                            s[(i-1,j-1)]
                            )
            if s[(i,j)] == s[(i-1,j)]:
                backtrack[(i,j)] = 'down'
            if s[(i,j)] == s[(i,j-1)]:
                backtrack[(i,j)] = 'right'
            if s[(i,j)] == s[(i-1,j-1)] + 1:
                backtrack[(i,j)] = 'diag'
    return backtrack

def output_lcs(backtrack,v,i,j):
    if i==0 or j==0:
        return
    if backtrack[(i,j)] == 'down':
        output_lcs(backtrack,v,i-1,j)
    if backtrack[(i,j)] == 'right':
        output_lcs(backtrack,v,i,j-1)
    else:
        output_lcs(backtrack,v,i-1,j-1)
        print v[i-1]






