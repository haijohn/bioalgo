# -*- coding: utf-8 -*-

"""
Coursera Course: Bioinformatics Algorithms (Part 1)

https://class.coursera.org/bioinformatics-002

Unit1:  1. WHERE IN THE GENOME DOES DNA REPLICATION BEGIN?

find the replicate origin of a bacteria genome

"""


import sys
from collections import defaultdict


# find the most frequent words
def pattern_count(text, pattern):
    count = 0
    len_pattern = len(pattern)
    len_text = len(text)
    for i in range(len_text-len_pattern):
        if text[i:len_pattern+i] == pattern:
            count += 1
    return count


def frequent_words(text, k):
    """A naive implemtaion to find the most frequent words in a text"""
    counts = []
    for i in range(len(text)-k):
        pattern = text[i:i+k]
        count = pattern_count(text, pattern)
        counts.append(count)
    max_count = max(counts)
    max_kmers = set()
    for i in range(len(text)-k):
        if counts[i] == max_count:
            max_kmers.add(text[i:i+k])
    return max_kmers


# find most frequent words by indexing

alphabet_to_int = {"A": 0,
                   "C": 1,
                   "G": 2,
                   "T": 3}

int_to_alphabet = {0: "A",
                   1: "C",
                   2: "G",
                   3: "T"
                   }


def pattern_to_number(pattern):
    """
    """
    l = len(pattern)
    return sum(alphabet_to_int[pattern[i]]*4**(l-i-1)
               for i in range(l))


def number_to_pattern(num, k):
    pattern = []
    for i in range(k):
        mod = num % 4
        num = num / 4
        pattern.append(int_to_alphabet[mod])
    return "".join(pattern[::-1])


def compute_frequency(text, k):
    frequency_array = [0 for i in range(4**k)]
    for i in range(len(text)-k+1):
        pattern = text[i:i+k]
        j = pattern_to_number(pattern)
        frequency_array[j] += 1
    return frequency_array


def frequent_words_by_index(text, k):
    frequent_patterns = set([])
    frequency_array = compute_frequency(text, k)
    max_count = max(frequency_array)
    for i in range(4**k):
        if frequency_array[i] == max_count:
            pattern = number_to_pattern(i, k)
            frequent_patterns.add(pattern)
    return frequent_patterns

# find most frequent words by sorting


def frequent_words_by_sort(text, k):
    frequent_patterns = set([])
    indexes = []
    counts = []
    for i in range(len(text)-k+1):
        pattern = text[i:i+k]
        indexes.append(pattern_to_number(pattern))
        counts.append(1)
    sorted_index = sorted(indexes)
    for i in range(1, len(text)-k+1):
        if sorted_index[i] == sorted_index[i-1]:
            counts[i] = counts[i-1] + 1
    max_count = max(counts)
    for i in range(len(text)-k+1):
        if counts[i] == max_count:
            frequent_patterns.add(number_to_pattern(i, k))
    return frequent_patterns

# find most frequent words by hashing


def frequent_words_by_hash(text, k):
    pattern_count_hash = defaultdict(int)
    frequent_patterns = set([])
    for i in range(len(text)-k+1):
        pattern = text[i:i+k]
        pattern_count_hash[pattern] += 1
    max_count = max(pattern_count_hash.values())
    for pattern, count in pattern_count_hash.items():
        if count == max_count:
            frequent_patterns.add(pattern)
    return frequent_patterns


def frequent_words_by_hash_thre(text, k, t):
    """t is the cutoff """
    pattern_count_hash = defaultdict(int)
    frequent_patterns = set([])
    for i in range(len(text)-k+1):
        pattern = text[i:i+k]
        pattern_count_hash[pattern] += 1
    for pattern, count in pattern_count_hash.items():
        if count >= t:
            frequent_patterns.add(pattern)
    return frequent_patterns


def pattern_match(genome, pattern):
    """Input: Two strings, Pattern and Genome.
       return: All starting positions where Pattern appears as a substring of Genome."""
    genome_size = len(genome)
    pattern_size = len(pattern)
    match_positions = []
    for i in range(genome_size - pattern_size+1):
        if genome[i:i+pattern_size] == pattern:
            match_positions.append(i)
    return match_positions


def find_clump(genome, l, k, t):
    """Clump Finding Problem: Find patterns forming clumps in a string.
       Input: A string Genome, and integers k, l, and t.
       Output: All distinct k-mers forming (L, t)-clumps in Genome."""
    clump_kmers = set([])
    genome_len = len(genome)
    for i in range(genome_len-l+1):
        window = genome[i:i+l]
        patterns = frequent_words_by_hash_thre(window, k, t)
        clump_kmers |= patterns
    return clump_kmers

# get minimal skew position of a genome


def min_skew_position(genome):
    genome_size = len(genome)
    G_minus_C = [0]
    for i in range(0, genome_size):
        if genome[i] == "C":
            G_minus_C.append(G_minus_C[i]-1)
        elif genome[i] == "G":
            G_minus_C.append(G_minus_C[i]+1)
        else:
            G_minus_C.append(G_minus_C[i])
    min_diff = min(G_minus_C)
    min_indexes = []
    for i, num in enumerate(G_minus_C):
        if num == min_diff:
            min_indexes.append(i)
    return min_indexes

# get reverse complementary of a sequence
complementary_table = {
    "A": "T",
    "C": "G",
    "G": "C",
    "T": "A"
    }


def reverse_complement(pattern):
    return "".join([complementary_table[N] for N in pattern][::-1])

# get hamming distance of two string


def hamming_distance(s1, s2):
    return sum(ch1 != ch2 for ch1, ch2 in zip(s1, s2))


def approximate_pattern_match(pattern, text, d):
    """Find all approximate occurrences of a pattern in a string.
       Input: Strings Pattern and Text along with an integer d.
       Output: All starting positions where Pattern appears as
               a substring of Text with at most d mismatches."""
    positions = []
    len_pattern = len(pattern)
    len_text = len(text)
    for i in range(len_text-len_pattern+1):
        if hamming_distance(pattern, text[i:i+len_pattern]) <= d:
            positions.append(i)
    return positions


def approximate_pattern_count(text, pattern, d):
    return len(approximate_pattern_match(pattern, text, d))


def immediate_neighbors(pattern):
    """generate the 1-neigborhood of Pattern"""
    neighbors = set([pattern])
    for i in range(len(pattern)):
        current = pattern[i]
        before = pattern[:i]
        after = pattern[i+1:]
        for m in "ATCG":
            if m != current:
                neighbor = "".join([before, m, after])
                neighbors.add(neighbor)
    return neighbors


def iterative_neighbors(pattern, d):
    neighbors = set([pattern])
    for i in range(d):
        neighs = neighbors.copy()
        for pat in neighs:
            neighbors.update(immediate_neighbors(pat))
    return neighbors


def recursive_neighbors(pattern, d):
    pass


def frequent_words_with_mismatch_rc(text, k, d):
    """Find the most frequent k-mers with mismatches in a string.
       Input: A string Text as well as integers k and d. (You may assume k ≤ 12 and d ≤ 3.)
       Output: All most frequent k-mers with up to d mismatches in T"""
    frequent_patterns = set()
    close_array = [0 for i in range(4**k)]
    frequent_array = [0 for i in range(4**k)]
    for i in range(len(text)-k+1):
        pattern = text[i:i+k]
        neighbors = iterative_neighbors(pattern, d)
        for neighbor in neighbors:
            close_array[pattern_to_number(neighbor)] = 1
    for i in range(4**k):
        if close_array[i] == 1:
            pattern = number_to_pattern(i, k)
            frequent_array[i] = approximate_pattern_count(text, pattern, d) + \
                                approximate_pattern_count(text,
                                                          reverse_complement(pattern),
                                                          d)
    max_count = max(frequent_array)
    for i in range(4**k):
        if frequent_array[i] == max_count:
            pattern = number_to_pattern(i, k)
            frequent_patterns.add(pattern)
    return frequent_patterns


def frequent_words_with_mismatch_by_sort(text, k):
    pass
