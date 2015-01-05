# -*- coding: utf-8 -*-

"""

Unit5: How Do We Compare Sequence ?

"""

from utils import *
import sys
sys.setrecursionlimit(10000)

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
    """ use dynamic programming solve manhatten tourist problem"""
    s = {}
    s[(0,0)] = 0
    for i in range(1, n+1):
        s[(i,0)] = s[(i-1,0)] + down_matrix[i-1][0]
    for j in range(1, m+1):
        s[(0,j)] = s[(0,j-1)] + right_matrix[0][j-1]
    for i in range(1, n+1):
        for j in range(1, m+1):
            s[(i,j)] = max([
                            s[(i-1,j)] + down_matrix[i-1][j],
                            s[(i,j-1)] + right_matrix[i][j-1]
                           ])
    return s[n,m]
# end Manhattan tourist problem


def lcs_backtrack(v,w):
    m = len(v)
    n = len(w)
    s = {}
    s[(0,0)] = 0
    backtrack = {}
    for i in range(1,m+1):
        s[(i,0)] = 0
        backtrack[(i,0)] = 'down'
    for j in range(1,n+1):
        s[(0,j)] = 0
        backtrack[(0,j)] = 'right'
    for i in range(1,m+1):
        for j in range(1,n+1):
            if v[i-1] == w[j-1]:
                s[(i,j)] = max(s[(i-1,j)],
                                s[(i,j-1)],
                                s[(i-1,j-1)] +1 
                               )
            else:
                s[(i,j)] = max(s[(i-1,j)],
                                s[(i,j-1)],
                                s[(i-1,j-1)]
                               )
            if s[(i,j)] == s[(i-1,j)]:
                backtrack[(i,j)] = 'down'
            elif s[(i,j)] == s[(i,j-1)]:
                backtrack[(i,j)] = 'right'
            else:
                backtrack[(i,j)] = 'diag'
    return backtrack
          

def output_lcs(backtrack,v,i,j,s=None):
    if s is None:
        s = []
    if i==0 or j==0:
        return
    if backtrack[(i,j)] == 'down':
        output_lcs(backtrack,v,i-1,j,s)
    elif backtrack[(i,j)] == 'right':
        output_lcs(backtrack,v,i,j-1,s)
    else:
        output_lcs(backtrack,v,i-1,j-1,s)
	s.append(v[i-1])
    return s
        

#c = read_content('1.txt')
#v = c[0]
#w = c[1]
#b = lcs_backtrack(v,w)
#s = output_lcs(b,v,len(v),len(w))
#with open('2.txt','w') as f:
#    print>>f,''.join(s)

def parse_blosum62(blosum_file):
    blosum_matrix = {}
    with open(blosum_file) as f:
       header = f.readline().strip().split()
       for line in f:
           line = line.strip().split()
           c = line[0]
           for i,score in enumerate(line[1:]):
               blosum_matrix[(c,header[i])] = int(score)
    return blosum_matrix
               


def global_alignment(v,w,blosum62,gap_penalty=-5):
    m = len(v)
    n = len(w)
    s = {}
    s[(0,0)] = 0
    backtrack = {}
    for i in range(1,m+1):
        s[(i,0)] = s[(i-1,0)] + gap_penalty
        backtrack[(i,0)] = 'down'
    for j in range(1,n+1):
        s[(0,j)] = s[(0,j-1)] + gap_penalty
        backtrack[(0,j)] = 'right'
    for i in range(1,m+1):
        for j in range(1,n+1):
            s[(i,j)] = max(s[(i-1,j)] + gap_penalty,
                           s[(i,j-1)] + gap_penalty,
                           s[(i-1,j-1)] + blosum62[(v[i-1],w[j-1])],
                          )
            if s[(i,j)] == s[(i-1,j)] + gap_penalty:
                backtrack[(i,j)] = 'down'
            elif s[(i,j)] == s[(i,j-1)] + gap_penalty:
                backtrack[(i,j)] = 'right'
            else:
                backtrack[(i,j)] = 'diag'
    return backtrack,s[m,n]
          
def print_alignment(backtrack,v,w,i,j,s=None,p=None):
    if s is None:
        s = []
    if p is None:
        p = []
    if i==0 and j==0:
        return
    if backtrack[(i,j)] == 'down':
        print_alignment(backtrack,v,w,i-1,j,s,p)
        p.append('-')
        s.append(v[i-1])
    elif backtrack[(i,j)] == 'right':
        print_alignment(backtrack,v,w,i,j-1,s,p)
        s.append('-')
        p.append(w[j-1])
    else:
        print_alignment(backtrack,v,w,i-1,j-1,s,p)
	s.append(v[i-1])
	p.append(w[j-1])
    return s,p


m = parse_blosum62('BLOSUM62.txt')
c = read_content('1.txt')
v = c[0]
w = c[1]
b,score = global_alignment(v,w,m)
#print b
s,p = print_alignment(b,v,w,len(v),len(w))
q = output_lcs(b,v,len(v),len(w))
with open('2.txt','w') as f:
    print>>f, score
    print>>f, ''.join(s)
    print>>f, ''.join(p)





