
"""
Coursera Course: Bioinformatics Algorithms (Part 1)

https://class.coursera.org/bioinformatics-002

Unit3:  Hunting for Regulatory Motifs


"""
from __future__ import division
from oricfinder import neighbors
from oricfinder import hamming_distance
from oricfinder import number_to_pattern
from functools import reduce
import random

def generate_kmers(dna, k):
    return [dna[i:k+i] for i in range(len(dna)-k+1)]

def motif_enumeration(dnas, k, d):
    """Input: Integers k and d, followed by a collection of strings Dna.
       Output: All (k, d)-motifs in Dna.
    """
    return reduce(lambda x, y: x & y,
                    (reduce(lambda x, y: x + y,
                          (neighbors(kmer,d) for kmer in generate_kmers(dna,k)))
                                for dna in dnas))

def distance_patter_string(pattern, dnas):
    """Input: A string Pattern followed by a collection of strings Dna.
       Output: d(Pattern, Dna).
    """
    return reduce(lambda x, y: x + y, (
                    min(hamming_distance(pattern, kmer)
                        for kmer in generate_kmers(dna, len(pattern)))
                            for dna in dnas))

def median_string(dnas, k):
    return min(((number_to_pattern(i,k),
                 distance_patter_string(number_to_pattern(i,k), dnas))
                        for i in range(4**k)),
                key = lambda x: x[1])[0]

def profile_most_probable(dna, k, profile):
    """Input: A string Text, an integer k, and a 4 * k matrix Profile.
       Output: A Profile-most probable k-mer in Text.
    """
    n2i = {'A':0,'C':1,'G':2,'T':3}
    return max(((kmer,reduce(lambda x,y: x*y, [profile[n2i[kmer[i]]][i]
                    for i in range(k)]))
                        for kmer in generate_kmers(dna, k)),
               key=lambda x: x[1])[0]

def get_profile(motifs):
    k = len(motifs[0])
    t = len(motifs)
    # add 1 to apply Laplace's Rule of Succession
    return [[([motif[i] for motif in motifs].count(N)+1)/t
                for i in range(k)]
                    for N in 'ACGT']

def score(motifs):
    k = len(motifs[0])
    t = len(motifs)
    profile = get_profile(motifs)
    return sum([t-max([p[i] for p in profile])*t for i in range(k)])

def greedy_motif_search(dnas, k, t):
    kmerss = [generate_kmers(dna, k) for dna in dnas]
    best_motifs = [kmers[0] for kmers in kmerss]
    for kmers_1 in kmerss[0]:
        motifs = [kmers_1]
        for i in range(1, t):
            profile = get_profile(motifs)
            motifs.append(profile_most_probable(dnas[i], k, profile))
        if score(motifs) < score(best_motifs):
            best_motifs = motifs
    return best_motifs

def randomized_motif_search(dnas, k, t):
    kmerss = [generate_kmers(dna, k) for dna in dnas]
    best_motifs = [kmers[random.randint(0,len(kmers)-1)] for kmers in kmerss]
    while True:
        profile = get_profile(best_motifs)
        motifs = [profile_most_probable(dna, k, profile) for dna in dnas]
        if score(motifs) < score(best_motifs):
            best_motifs = motifs
        else:
            return best_motifs


def gibbs_sampler(dnas, k, t, N):
    kmerss = [generate_kmers(dna, k) for dna in dnas]
    best_motifs = [kmers[random.randint(0,len(kmers)-1)] for kmers in kmerss]
    motifs = best_motifs[:]
    for j in range(N):
        i = random.randint(0,t-1)
        motifs.pop(i)
        profile = get_profile(motifs)
        motifs.insert(i, profile_most_probable(dnas[i], k, profile))
        if score(motifs) < score(best_motifs):
            best_motifs = motifs
    return best_motifs

def simulate(num_trail, dnas, k, t, N, randomized_search):
    return min((randomized_search(dnas, k, t, N) for i in range(num_trail)),
               key = lambda x: score(x))










