# -*- coding: utf-8 -*-

"""
Coursera Course: Bioinformatics Algorithms (Part 1) 

https://class.coursera.org/bioinformatics-002

Unit2: How Do We Sequence Antibiotics? (Brute Force Algorithms)

"""
from utils import rna_codon_table
from utils import rna_codon_reverse
from oricfinder import reverse_complement

def translate(RNA):
    if len(RNA) % 3 != 0:
        raise Exception("length is not rigth")
    return "".join(rna_codon_table[RNA[i:i+3]] for i in range(0,len(RNA),3))

def transcribe(DNA):
    return "".join("U" if n=="T" else n for n in DNA)

def peptide_decode(DNA, peptide):
    len_peptide = len(peptide)
    len_DNA = len(DNA)
    len_DNA_fragment = len_peptide * 3
    encodes = []
    for i in range(0, len_DNA-len_DNA_fragment+1):
        DNA_fragment = DNA[i:i+len_DNA_fragment]
        rc_DNA_fragment = reverse_complement(DNA_fragment)
    	RNA_fragment = transcribe(DNA_fragment)
        rc_RNA_fragment = transcribe(rc_DNA_fragment)
        if translate(RNA_fragment) == peptide or translate(rc_RNA_fragment) == peptide:
            encodes.append(DNA_fragment)
    return encodes

