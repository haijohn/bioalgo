# -*- coding: utf-8 -*-

"""
Coursera Course: Bioinformatics Algorithms (Part 1) 

https://class.coursera.org/bioinformatics-002

Unit2: How Do We Sequence Antibiotics? (Brute Force Algorithms)

"""
from utils import rna_codon_table
from utils import integer_mass_table
from oricfinder import reverse_complement

def translate(rna):
    if len(rna) % 3 != 0:
        raise Exception("length is not right")
    return "".join(rna_codon_table[rna[i:i+3]] for i in range(0,len(rna),3))

def transcribe(dna):
    return "".join("U" if n=="T" else n for n in dna)

def peptide_decode(dna, peptide):
    """find the corresponding encode of a peptide
       Input: a dna sequence, a peptide sequence
       Output: find substring in the dna sequence that encodes the peptide"""
    len_peptide = len(peptide)
    len_dna = len(dna)
    len_dna_fragment = len_peptide * 3
    dna_encodes = []
    for i in range(0, len_dna-len_dna_fragment+1):
        dna_fragment = dna[i:i+len_DNA_fragment]
        rc_dna_fragment = reverse_complement(dna_fragment)
    	rna_fragment = transcribe(dna_fragment)
        rc_rna_fragment = transcribe(rc_dna_fragment)
        if translate(rna_fragment) == peptide or translate(rc_rna_fragment) == peptide:
            encodes.append(dna_fragment)
    return encodes

def peptide_to_integer(peptide):
    """get the mass of a peptide"""
    return sum(integer_mass_table[a] for a in peptide)

def generate_theoretical_spectrum(peptide):
    """Generate the theoretical spectrum of a cyclic peptide.
       Input: An amino acid string Peptide.
       Output: Cyclospectrum(Peptide)"""
    spectrum = [0, peptide_to_integer(peptide)]
    len_pep = len(peptide)
    for i in range(1, len_pep):
        for j in range(0, len_pep):
            latter = i + j
            if latter <= len_pep:
                sub_pep = peptide[j:latter]
                spectrum.append(peptide_to_integer(sub_pep))
            else:
                sub_pep = peptide[j:] + peptide[0:latter-len_pep]
                spectrum.append(peptide_to_integer(sub_pep))
    return sorted(spectrum)
            


