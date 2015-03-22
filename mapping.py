
'''
1. How Do We Locate Disease-Causing Mutations? 
'''
from __future__ import print_function
from collections import OrderedDict

def trie_construction(patterns):
    """ packing string patterns into a single trie
    params: patterns
            type: list or tuple
    return: a trie 
            type: dict of dict
    >>> patterns = ["ATAGA", "ATC", "GAT"]
    >>> trie_construction(patterns)
    >>> {0:{"A":1}, 1:{"T":1}}
    """
    trie = OrderedDict()
    node_index = 0
    for pattern in patterns:
        current_node = 0
        for letter in pattern:
            children = trie.get(current_node, False)
            if children:
                child =  children.get(letter, False)
                if child:
                    current_node = child
                else:
                    node_index += 1
                    children[letter] = node_index
                    current_node = node_index
            else:
                trie[current_node] = {}
                node_index += 1
                trie[current_node][letter] = node_index
                current_node = node_index
    return trie

def print_trie(trie, filename):
    with open(filename,'wb') as of:
        for node in trie:
            for child in trie[node].items():
                print(str(node)+'->'+str(child[1])+":"+child[0],file=of)
