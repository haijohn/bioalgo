# -*- coding: utf-8 -*-

"""

Unit5: How Do We Compare Sequence ?

"""

from utils import *
from graph import *
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
    """ use botton-up dynamic programming solve manhatten tourist problem"""
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


def toplogical_ordering(graph, src):
    ordering = [src]
    for edge in graph.out_edges(src):
        graph.remove_edge(edge)
    graph.remove_node(src)
    candidates = [node for node in graph.get_nodes() 
                          if graph.indegree(node) == 0  ]
    while candidates:
        candidate = candidates.pop()
        ordering.append(candidate)
        for edge in graph.out_edges(candidate):
            graph.remove_edge(edge)
        graph.remove_node(candidate)
        candidates = [node for node in graph.get_nodes() 
                          if graph.indegree(node) == 0]
    return ordering


def build_graph(graph_file):
    g = DiGraph()
    with open(graph_file) as f:
        source = f.readline().strip()
        sink = f.readline().strip()
        for line in f:
            src,dest = line.strip().split('->')
            dest,weight = dest.split(':')
            src = Node(src)
            dest = Node(dest)
            edge = WeightedEdge(src,dest,weight)
            if not g.has_node(src):
                g.add_node(src)
            if not g.has_node(dest):
                g.add_node(dest)
            g.add_edge(edge)
    return Node(source), Node(sink), g

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
                                #s[(i-1,j-1)]
                               )
            if s[(i,j)] == s[(i-1,j)]:
                backtrack[(i,j)] = 'down'
            elif s[(i,j)] == s[(i,j-1)]:
                backtrack[(i,j)] = 'right'
            else:
                backtrack[(i,j)] = 'match'
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
    elif backtrack[(i,j)] == 'mismatch':
        output_lcs(backtrack,v,i-1,j-1,s)
    else:
        output_lcs(backtrack,v,i-1,j-1,s)
	s.append(v[i-1])
    return s
        
def parse_score_matrix(score_file):
    blosum_matrix = {}
    with open(score_file) as f:
       header = f.readline().strip().split()
       for line in f:
           line = line.strip().split()
           c = line[0]
           for i,score in enumerate(line[1:]):
               blosum_matrix[(c,header[i])] = int(score)
    return blosum_matrix
               


def global_alignment(v, w, score_matrix, gap_penalty=-5):
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
                           s[(i-1,j-1)] + score_matrix[(v[i-1],w[j-1])],
                          )
            if s[(i,j)] == s[(i-1,j)] + gap_penalty:
                backtrack[(i,j)] = 'down'
            elif s[(i,j)] == s[(i,j-1)] + gap_penalty:
                backtrack[(i,j)] = 'right'
            else:
                backtrack[(i,j)] = 'diag'
    return backtrack,s[m,n]
          
def local_alignment(v,w,score_matrix,gap_penalty=-5):
    m = len(v)
    n = len(w)
    s = {}
    max_score = 0
    max_position = (0,0)
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
            s[(i,j)] = max(
                           0,
                           s[(i-1,j)] + gap_penalty,
                           s[(i,j-1)] + gap_penalty,
                           s[(i-1,j-1)] + score_matrix[(v[i-1],w[j-1])],
                          )
            if s[(i,j)] == s[(i-1,j)] + gap_penalty:
                backtrack[(i,j)] = 'down'
            elif s[(i,j)] == s[(i,j-1)] + gap_penalty:
                backtrack[(i,j)] = 'right'
            else:
                backtrack[(i,j)] = 'diag'
    return backtrack, s
          
def print_alignment(backtrack, v, w, i, j, s=None, p=None):
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


def print_local_alignment(backtrack,v, w, i, j, s=None, p=None):
    if s is None:
        s = []
    if p is None:
        p = []
    if scores[(i,j)] == 0: #global ????
        return
    if backtrack[(i,j)] == 'down':
        print_local_alignment(backtrack,v,w,i-1,j,s,p)
        p.append('-')
        s.append(v[i-1])
    elif backtrack[(i,j)] == 'right':
        print_local_alignment(backtrack,v,w,i,j-1,s,p)
        s.append('-')
        p.append(w[j-1])
    else:
        print_local_alignment(backtrack,v,w,i-1,j-1,s,p)
        s.append(v[i-1])
        p.append(w[j-1])
    return s,p


def solve_local_alignment(input, output):
    #m = parse_blosum62('BLOSUM62.txt')
    c = read_content(input)
    v = c[0]
    w = c[1]
    #v = 'AAAAMEANLY'
    #w = 'FFFFPENALTY'
    m = parse_score_matrix('PAM250_1.txt')
    b,scores = local_alignment(v,w,m)
    max_p = reduce(lambda x,y: y if x[1] < y[1] else x,scores.items())
    (i,j),score = max_p
    #print b
    s,p = print_local_alignment(b, v, w, i, j)
    #q = output_lcs(b,v,i,j)
    with open(output,'w') as f:
        print>>f, score
        print>>f, ''.join(s)
        print>>f, ''.join(p)

def edit_distance(v,w):
    """edit distance of two string"""
    m = len(v)
    n = len(w)
    s = {}
    s[(0,0)] = 0
    backtrack = {}
    for i in range(1,m+1):
        s[(i,0)] = i
    for j in range(1,n+1):
        s[(0,j)] = j
    for i in range(1,m+1):
        for j in range(1,n+1):
            if v[i-1] == w[j-1]:
                s[(i,j)] = min(s[(i-1,j)] + 1,
                                s[(i,j-1)] + 1,
                                s[(i-1,j-1)] 
                               )
            else:
                s[(i,j)] = min(s[(i-1,j)] + 1,
                                s[(i,j-1)] + 1,
                                s[(i-1,j-1)] + 1
                               )
    return s[m,n]

def fitting_alignment(v, w, gap_penalty=-1):
    m,n = len(v),len(w)
    s = {}
    max_score = 0
    max_position = (0,0)
    s[(0,0)] = 0
    backtrack = {}
    for i in range(1,m+1):
        s[(i,0)] = 0
        backtrack[(i,0)] = 'down'
    for j in range(1,n+1):
        s[(0,j)] = s[(0,j-1)] + gap_penalty
        backtrack[(0,j)] = 'right'
    for i in range(1,m+1):
        for j in range(1,n+1):
            if v[i-1] == w[j-1]:
                s[(i,j)] = max(
#                           0,
                           s[(i-1,j)] + gap_penalty,
                           s[(i,j-1)] + gap_penalty,
                           s[(i-1,j-1)] + 1
                          )
            else:
                s[(i,j)] = max(
 #                          0,
                           s[(i-1,j)] + gap_penalty,
                           s[(i,j-1)] + gap_penalty,
                           s[(i-1,j-1)] + gap_penalty
                          )
                
            if s[(i,j)] == s[(i-1,j)] + gap_penalty:
                backtrack[(i,j)] = 'down'
            elif s[(i,j)] == s[(i,j-1)] + gap_penalty:
                backtrack[(i,j)] = 'right'
            else:
                backtrack[(i,j)] = 'diag'
    return backtrack, s
          
def print_fitting_alignment(backtrack,v, w, i, j, s=None, p=None):
    if s is None:
        s = []
    if p is None:
        p = []
    if j == 0: #global ????
        return
    if backtrack[(i,j)] == 'down':
        print_fitting_alignment(backtrack,v,w,i-1,j,s,p)
        p.append('-')
        s.append(v[i-1])
    elif backtrack[(i,j)] == 'right':
        print_fitting_alignment(backtrack,v,w,i,j-1,s,p)
        s.append('-')
        p.append(w[j-1])
    else:
        print_fitting_alignment(backtrack,v,w,i-1,j-1,s,p)
        s.append(v[i-1])
        p.append(w[j-1])
    return s,p

def solve_fitting_alignment():
    c = read_content('1.txt')
    v = c[0]
    w = c[1]
    #v = 'GTAGGCTTAAGGTTA'
    #w = 'TAGATA'
    lw = len(w)
    b,scores = fitting_alignment(v,w)
    #print scores
    margins = [item for item in scores.items() if item[0][1] == len(w)]
    max_p = reduce(lambda x,y: y if x[1] < y[1] else x,margins)
    #print max_p
    (i,j),score = max_p
    s,p = print_fitting_alignment(b, v, w, i, j)
    print score
    print ''.join(s)
    print ''.join(p)


def solve_overlap_alignment():
    c = read_content('1.txt')
    v = c[0]
    w = c[1]
    #v = 'PAWHEAE'
    #w = 'HEAGAWGHEE'
    lw = len(w)
    b,scores = fitting_alignment(v,w,gap_penalty=-2)
    #print scores
    margins = [item for item in scores.items() if item[0][0] == len(v)]
    max_p = reduce(lambda x,y: y if x[1] < y[1] else x,margins)
    #print max_p
    (i,j),score = max_p
    s,p = print_fitting_alignment(b, v, w, i, j)
    print score
    print ''.join(s)
    print ''.join(p)


def affine_gap_panelty(v, w, score_matrix, gap_penalty=-5, extension_panelty=-1):
    """ 3 level manhatten """
    m,n = len(v),len(w)
    sl = {} #lower score
    sm = {} #middle score
    su = {} #up score
    sl[(0,0)] = len(w)*gap_penalty
    sm[(0,0)] = 0
    su[(0,0)] = len(w)*gap_penalty
    backtrack_l = {}
    backtrack_m = {}
    backtrack_u = {}
    for i in range(1, m+1):
        su[(i,0)] = len(w)*gap_penalty
        sl[(i,0)] = gap_penalty + (i-1)*extension_panelty
        sm[(i,0)] = sl[(i,0)]
        if i == 1:
            backtrack_l[(i,0)] = "open" 
        else:
            backtrack_l[(i,0)] = "extention"
        backtrack_m[(i,0)] = "down close"
    for j in range(1, n+1):
        sl[(0,j)] = len(w)*gap_penalty
        su[(0,j)] = gap_penalty + (i-1)*extension_panelty   
        sm[(0,j)] = su[(0,j)]
        if j == 1:
            backtrack_u[(0,j)] = "open" 
        else:
            backtrack_u[(0,j)] = "extention"
        backtrack_m[(0,j)] = "close"
    for i in range(1,m+1):
        for j in range(1,n+1):
            sl[(i,j)] = max(
                          sl[(i-1,j)] + extension_panelty,
                          sm[(i-1,j)] + gap_penalty
                         )
            if sl[(i,j)] == sl[(i-1,j)] + extension_panelty:
                backtrack_l[(i,j)] = 'extention'
            else:
                backtrack_l[(i,j)] = 'open'
            su[(i,j)] = max(
                          su[(i,j-1)] + extension_panelty,
                          sm[(i,j-1)] + gap_penalty
                         )
            if su[(i,j)] == su[(i,j-1)] + extension_panelty:
                backtrack_u[(i,j)] = 'extention'
            else:
                backtrack_u[(i,j)] = 'open'
            sm[(i,j)] = max(
                          sm[(i-1,j-1)] + score_matrix[(v[i-1],w[j-1])],
                          sl[(i,j)],
                          su[(i,j)]
                         )
            if sm[(i,j)] == sm[(i-1,j-1)] + score_matrix[(v[i-1],w[j-1])]:
                backtrack_m[(i,j)] = 'diag'
            elif sm[(i,j)] == sl[(i,j)]:
                backtrack_m[(i,j)] = 'down close'
            elif sm[(i,j)] == su[(i,j)]:
                backtrack_m[(i,j)] = 'up close'
    return sm[(m,n)], backtrack_m, backtrack_l, backtrack_u

def print_affine_gap_panelty(backtrack_m, backtrack_l, backtrack_u, v, w, i, j, state='m', s=None, p=None):
    if i==0 and j==0:
        return
    if s is None:
        s = []
    if p is None:
        p = []
    if state == 'm':
        if backtrack_m[(i,j)] == 'diag':
            print_affine_gap_panelty(backtrack_m, backtrack_l, backtrack_u, v, w, i-1, j-1, 'm', s, p)
            s.append(v[i-1])
            p.append(w[j-1])
        elif backtrack_m[(i,j)] == 'up close':
            print_affine_gap_panelty(backtrack_m, backtrack_l, backtrack_u, v, w, i, j, 'u', s, p)
        elif backtrack_m[(i,j)] == 'down close':
            print_affine_gap_panelty(backtrack_m, backtrack_l, backtrack_u, v, w, i, j, 'l', s, p)
    elif state == 'u':
        if backtrack_u[(i,j)] == 'open':
            print_affine_gap_panelty(backtrack_m, backtrack_l, backtrack_u, v, w, i, j-1, 'm', s, p)
        elif backtrack_u[(i,j)] == 'extention':
            print_affine_gap_panelty(backtrack_m, backtrack_l, backtrack_u, v, w, i, j-1, 'u', s, p)
        s.append('-')
        p.append(w[j-1])
    elif state == 'l':
        if backtrack_l[(i,j)] == 'open':
            print_affine_gap_panelty(backtrack_m, backtrack_l, backtrack_u, v, w, i-1, j, 'm', s, p)
        elif backtrack_u[(i,j)] == 'extention':
            print_affine_gap_panelty(backtrack_m, backtrack_l, backtrack_u, v, w, i-1, j, 'l', s, p)
        s.append(v[i-1])
        p.append('-')
    return s,p        








