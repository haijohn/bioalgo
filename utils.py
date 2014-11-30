# -*- coding: utf-8 -*-

"""
io utils function for read dataset and write result
"""
from __future__ import print_function
import re


def read_content(filename, numline=2):
    if not isinstance(filename, file):
        f = open(filename)
    else:
        f = filename
    content = []
    for i in range(numline):
        line = f.readline().strip()
        if re.match("\d+", line):
            if re.match("\d+\s\d+", line):
                line = [int(i) for i in line.split(" ")]
            elif re.match("\d+\.\d+\s\d+\.\d+", line):
                line = [float(i) for i in line.split(" ")]
            else:
                line = int(line)
        content.append(line)
    f.close()
    return content if numline > 1 else content[0]

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

integer_mass_table = {'A': 71,
                      'C': 103,
                      'D': 115,
                      'E': 129,
                      'F': 147,
                      'G': 57,
                      'H': 137,
                      'I': 113,
                      'K': 128,
                      'L': 113,
                      'M': 131,
                      'N': 114,
                      'P': 97,
                      'Q': 128,
                      'R': 156,
                      'S': 87,
                      'T': 101,
                      'V': 99,
                      'W': 186,
                      'Y': 163}


