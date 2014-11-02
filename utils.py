# -*- coding: utf-8 -*-

"""
io utils function for read dataset and write result
"""
from __future__ import print_function


def read_content(filename, numline=2):
    if not isinstance(filename, file):
        f = open(filename)
    else:
        f = filename
    content = []
    for i in range(numline):
        line = f.readline().strip()
        content.append(int(line) if line.isdigit() else line)
    f.close()
    return tuple(content) if numline > 1 else content[0]

def write_result(filename, content, sep=" "):
    if not isinstance(filename, file):
        f = open(filename, "w")
    else:
        f = filename
    try:
        content = iter(content)
    except TypeError:
        print(content, file=f)
    else:
    	print(sep.join(str(c) if not isinstance(c,str) else c for c \
                        in content), file=f)
    f.close()

rna_codon_table = {'AAA': 'K',
                   'AAC': 'N',
                   'AAG': 'K',
                   'AAU': 'N',
                   'ACA': 'T',
                   'ACC': 'T',
                   'ACG': 'T',
                   'ACU': 'T',
                   'AGA': 'R',
                   'AGC': 'S',
                   'AGG': 'R',
                   'AGU': 'S',
                   'AUA': 'I',
                   'AUC': 'I',
                   'AUG': 'M',
                   'AUU': 'I',
                   'CAA': 'Q',
                   'CAC': 'H',
                   'CAG': 'Q',
                   'CAU': 'H',
                   'CCA': 'P',
                   'CCC': 'P',
                   'CCG': 'P',
                   'CCU': 'P',
                   'CGA': 'R',
                   'CGC': 'R',
                   'CGG': 'R',
                   'CGU': 'R',
                   'CUA': 'L',
                   'CUC': 'L',
                   'CUG': 'L',
                   'CUU': 'L',
                   'GAA': 'E',
                   'GAC': 'D',
                   'GAG': 'E',
                   'GAU': 'D',
                   'GCA': 'A',
                   'GCC': 'A',
                   'GCG': 'A',
                   'GCU': 'A',
                   'GGA': 'G',
                   'GGC': 'G',
                   'GGG': 'G',
                   'GGU': 'G',
                   'GUA': 'V',
                   'GUC': 'V',
                   'GUG': 'V',
                   'GUU': 'V',
                   'UAA': '',
                   'UAC': 'Y',
                   'UAG': '',
                   'UAU': 'Y',
                   'UCA': 'S',
                   'UCC': 'S',
                   'UCG': 'S',
                   'UCU': 'S',
                   'UGA': '',
                   'UGC': 'C',
                   'UGG': 'W',
                   'UGU': 'C',
                   'UUA': 'L',
                   'UUC': 'F',
                   'UUG': 'L',
                   'UUU': 'F'}

rna_codon_reverse = {'A': ['GCA', 'GCG', 'GCC', 'GCU'], '': ['UGA', 'UAA', 'UAG'], 'C': ['UGU', 'UGC'], 'E': ['GAA', 'GAG'], 'D': ['GAC', 'GAU'], 'G': ['GGU', 'GGG', 'GGA', 'GGC'], 'F': ['UUU', 'UUC'], 'I': ['AUA', 'AUC', 'AUU'], 'H': ['CAC', 'CAU'], 'K': ['AAG', 'AAA'], 'M': ['AUG'], 'L': ['CUU', 'CUG', 'CUA', 'CUC', 'UUG', 'UUA'], 'N': ['AAC', 'AAU'], 'Q': ['CAG', 'CAA'], 'P': ['CCC', 'CCA', 'CCU', 'CCG'], 'S': ['AGC', 'AGU', 'UCU', 'UCG', 'UCC', 'UCA'], 'R': ['AGG', 'AGA', 'CGA', 'CGC', 'CGG', 'CGU'], 'T': ['ACC', 'ACA', 'ACU', 'ACG'], 'W': ['UGG'], 'V': ['GUU', 'GUC', 'GUG', 'GUA'], 'Y': ['UAU', 'UAC']}
