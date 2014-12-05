# -*- coding: utf-8 -*-

"""
Coursera Course: Bioinformatics Algorithms (Part 1)

https://class.coursera.org/bioinformatics-002

Unit1:  4. HOW DO WE ASSEMBLE GENOMES?

find the replicate origin of a bacteria genome

"""
def composition(dna, k):
    """Input: An integer k and a string Text.
        Output: Compositionk(Text), where the k-mers are written in lexicographic order."""
    res = [dna[i:k+i] for i in range(len(dna)-k+1)]
    res.sort()
    return res


