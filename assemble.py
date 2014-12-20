# -*- coding: utf-8 -*-

"""
Coursera Course: Bioinformatics Algorithms (Part 1)

https://class.coursera.org/bioinformatics-002

Unit:  4. HOW DO WE ASSEMBLE GENOMES?

find the replicate origin of a bacteria genome

"""
from collections import defaultdict
import random

def composition(k, dna):
    """Input: An integer k and a string Text.
       Output: Compositionk(Text), where the k-mers are written in lexicographic order.
    """
    res = [dna[i:k+i] for i in range(len(dna)-k+1)]
    res.sort()
    return res

def genome_path_to_genome(genome_path):
    """Input: A sequence of k-mers Pattern1, … ,Patternn such that the last
              k - 1 symbols of Patterni are equal to the first k-1 symbols of
              Patterni+1 for 1 ≤ i ≤ n-1.
       Output: A string Text of length k+n-1 such that the
               i-th k-mer in Text is equal to Patterni  (for 1 ≤ i ≤ n).
    """
    return genome_path[0] + ''.join(string[-1] for string in genome_path[1:])


def overlap_graph(kmers):
    """Input: A collection Patterns of k-mers.
       Output: The overlap graph Overlap(Patterns), in the form of an adjacency list."""
    overlaps = []
    for i in range(len(kmers)):
        for j in range(len(kmers)):
            if i != j and kmers[i][1:] == kmers[j][:-1]:
                overlaps.append((kmers[i],kmers[j]))
    overlaps.sort(key=lambda x: x[0])
    return overlaps

    #for overlap in overlaps:
    #    yield overlap[0] + ' -> ' + overlap[1]

def DeBruijnk(k, text):
    """ Input: An integer k and a string Text.
        Output: DeBruijnk(Text), in the form of an adjacency list.
    """
    k_compo = composition(k, text)
    debruijnk = defaultdict(list)
    for c in k_compo:
        debruijnk[c[:k-1]].append(c[1:])
    debruijnk = debruijnk.items()
    debruijnk.sort(key=lambda x: x[0])
    return debruijnk
    #for d in debruijnk:
    #    yield d[0] + ' -> ' + ','.join(d[1])

def DeBruijnk_from_kmers(k, kmers):
    """ Input: An integer k and kmers.
        Output: DeBruijnk(kmers), in the form of an adjacency list.
    """
    debruijnk = defaultdict(list)
    for c in kmers:
        debruijnk[c[:k-1]].append(c[1:])
    debruijnk = debruijnk.items()
    debruijnk.sort(key=lambda x: x[0])
    #return debruijnk
    for d in debruijnk:
        yield d[0] + ' -> ' + ','.join(d[1])

def build_digraph(adjacency):
    graph = {}
    for adj in adjacency:
        nodes = adj.split(' -> ')
        node1, node2s = nodes[0], nodes[1].split(',')
        graph[node1] = node2s
    return graph

def build_undirected_graph(digraph):
    graph = defaultdict(list)
    for node,childs in digraph.items():
        graph[node] += childs
        for n in childs:
            graph[n].append(node)
    return graph

def degrees(undirected_graph):
    return {node:len(undirected_graph[node]) for node in undirected_graph}

def get_odd_node(degrees):
    return [node for node in degrees if degrees[node]%2 == 1]

def eulerian_cycle(graph):
    """ Input: The adjacency list of an Eulerian directed graph.
        Output: An Eulerian cycle in this graph."""
    cycle = []
    while graph:
        if not cycle:        
            start_node = graph.keys()[0]
        current_node = start_node
        current_cycle = [current_node]
        while True:
            node = graph[current_node].pop(0)
            current_cycle.append(node)
            if not graph[current_node]:
                graph.pop(current_node) # remove node that has no child node 
            if node == start_node:
                break
            else:
                current_node = node
        if not cycle:
            cycle = current_cycle
        else:
            cycle = cycle[:idx] + current_cycle + cycle[idx+1:] # merge two cycle
        # get next start node which in the cycle and in the graph
        for i,cn in enumerate(cycle):
            if graph.get(cn, False):
                idx = i
                start_node = cn
                break
    return cycle

def eulerian_path(graph):
    """ Input: The adjacency list of an Eulerian directed graph.
        Output: An Eulerian path in this graph."""
    path = []
    undirected_graph = build_undirected_graph(graph)
    odd_nodes = get_odd_node(degrees(undirected_graph))
    start_node, end_node = odd_nodes
    if start_node not in graph:
        start_node, end_node = end_node, start_node
    #print odd_nodes
    while graph:
        current_node = start_node
        current_path = [current_node]
        while True:
            node = graph[current_node].pop(random.randrange(len(graph[current_node])))
            current_path.append(node)
            if not graph[current_node]:
                graph.pop(current_node) # remove node that has no child node 
            if node in (start_node, end_node):
                break
            else:
                current_node = node
        if not path:
            path = current_path
        else:
            path = path[:idx] + current_path + path[idx+1:] # merge two path
        # get next start node which in the path and in the graph
        for i,cn in enumerate(path):
            if graph.get(cn, False):
                idx = i
                start_node = cn
                break
    return path

def string_reconstruct(k, kmers):
    """ Input: An integer k followed by a list of k-mers Patterns.
     Output: A string Text with k-mer composition equal to Patterns."""
    debruijnk = DeBruijnk_from_kmers(k, kmers)
    digraph = build_digraph(debruijnk)
    path = eulerian_path(digraph)
    return genome_path_to_genome(path)

def binary_n(n):
    """generate binary string of length n"""
    binarys = []
    for i in range(2**n):
        binary = bin(i)[2:]
        if len(binary) < n:
            binary = '0'*(n-len(binary)) + binary
        binarys.append(binary)
    return binarys

def universal_circular_string(n):
    binarys = binary_n(n)
    debruijnk = DeBruijnk_from_kmers(n, binarys)
    digraph = build_digraph(debruijnk)
    path = eulerian_cycle(digraph)
    return genome_path_to_genome(path[:-(n-1)]) # n-1 because it's circular

def paired_composition(k, d, text):
    res = ['|'.join([text[i:i+k],text[i+d+k:i+2*k+d]]) for i in range(len(text)-2*k-d+1)]
    res.sort()
    return res

def DeBruijnk_from_paired_kmers(k, kmers):
    """ Input: An integer k and paired kmers seprated by | AAT|GGC.
        Output: DeBruijnk(kmers), in the form of an adjacency list.
    """
    debruijnk = defaultdict(list)
    for pkmer in kmers:
        k1, k2 = pkmer.split('|')
        prefix = '|'.join([k1[:k-1],k2[:-1]])
        suffix = '|'.join([k1[1:],k2[1:]])
        debruijnk[prefix].append(suffix)
    debruijnk = debruijnk.items()
    debruijnk.sort(key=lambda x: x[0])
    #return debruijnk
    for d in debruijnk:
        yield d[0] + ' -> ' + ','.join(d[1])

def string_reconstruct_from_paired_reads(k, d, kmers):
    """ Input: An integer k, integer d gap length, followed by a list of k-mers Patterns.
     Output: A string Text with paired k,d-mer composition equal to Patterns."""
    debruijnk = DeBruijnk_from_paired_kmers(k, kmers)
    digraph = build_digraph(debruijnk)
    path = eulerian_path(digraph)
    prefix_pattern = [p.split('|')[0] for p in path]
    suffix_pattern = [p.split('|')[1] for p in path]
    prefix_string = genome_path_to_genome(prefix_pattern)
    suffix_string = genome_path_to_genome(suffix_pattern)
    if prefix_string[k+d:] == suffix_string[:-(k+d)]:
        return prefix_string[:k+d] + suffix_string