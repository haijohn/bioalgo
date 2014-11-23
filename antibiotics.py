# -*- coding: utf-8 -*-

"""
Coursera Course: Bioinformatics Algorithms (Part 1)

https://class.coursera.org/bioinformatics-002

Unit2: How Do We Sequence Antibiotics? (Brute Force Algorithms)

"""
from collections import Counter
from utils import rna_codon_table
from utils import integer_mass_table
from oricfinder import reverse_complement


def translate(rna):
    if len(rna) % 3 != 0:
        raise Exception("length is not right")
    return "".join(rna_codon_table[rna[i:i+3]] for i in range(0, len(rna), 3))


def transcribe(dna):
    return "".join("U" if n == "T" else n for n in dna)


def peptide_decode(dna, peptide):
    """find the corresponding encode of a peptide
       Input: a dna sequence, a peptide sequence
       Output: find substring in the dna sequence that encodes the peptide"""
    len_peptide = len(peptide)
    len_dna = len(dna)
    len_dna_fragment = len_peptide * 3
    dna_encodes = []
    for i in range(0, len_dna-len_dna_fragment+1):
        dna_fragment = dna[i:i+len_dna_fragment]
        rc_dna_fragment = reverse_complement(dna_fragment)
        rna_fragment = transcribe(dna_fragment)
        rc_rna_fragment = transcribe(rc_dna_fragment)
        if translate(rna_fragment) == peptide or \
           translate(rc_rna_fragment) == peptide:
            dna_encodes.append(dna_fragment)
    return dna_encodes


def peptide_to_integer(peptide):
    """get the mass of a peptide"""
    return sum(integer_mass_table[a] for a in peptide)


def generate_cyclic_spectrum(peptide):
    """Generate the theoretical spectrum of a cyclic peptide.
       Input: An amino acid string Peptide.
       Output: Cyclospectrum(Peptide)"""
    if isinstance(peptide, str):
        spectrum = [0, peptide_to_integer(peptide)]
    else:
        spectrum = [0, sum(peptide)]
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
    spectrum.sort()
    return spectrum


def generate_linear_spectrum(peptide):
    if isinstance(peptide, str):
        spectrum = [0, peptide_to_integer(peptide)]
    else:
        spectrum = [0, sum(peptide)]
    len_pep = len(peptide)
    for i in range(0, len_pep):
        for j in range(i+1, len_pep+1):
            sub_pep = peptide[i:j]
            spectrum.append(peptide_to_integer(sub_pep))
    spectrum.sort()
    return spectrum

aas = integer_mass_table.keys()


def expand_peptide(peptides):
    return {peptide+a for a in aas for peptide in peptides}


def peptide_sequence(spectrum):
    """use branching and bounding to get the sequence from a full spectrum
       input: spectrum
       outpit: set of peptide sequence"""
    max_mass = max(spectrum)
    all_i = set(spectrum)
    peptides = {aa for s in spectrum for aa in integer_mass_table
                if integer_mass_table[aa] == s}
    output = set()
    while len(peptides) > 0:
        peptides = expand_peptide(peptides)
        copy = peptides.copy()
        for peptide in copy:
            mass = peptide_to_integer(peptide)
            current_spectrum = generate_cyclic_spectrum(peptide)
            if mass == max_mass:
                if current_spectrum == spectrum:
                    output.add(peptide)
                peptides.remove(peptide)
            else:
                # use linear_spectrum instead of cyclic spectrum
                # otherwise will over bounding
                linear_spectrum = generate_linear_spectrum(peptide)
                consistent = all(i in all_i for i in linear_spectrum)
                if not consistent:
                    peptides.remove(peptide)
    return output


def process_out(out):
    return {"-".join([str(integer_mass_table[i]) for i in aa]) for aa in out}


def compute_spectrum_score(peptide, spectrum, spec_type="cyclic"):
    """Compute the score of a cyclic peptide against a spectrum.
     Input: An amino acid string Peptide and a collection of integers Spectrum.
     Output: The score of Peptide against Spectrum, Score(Peptide, Spectrum)."""
    if spec_type == "cyclic":
        threoretical_spectrum = generate_cyclic_spectrum(peptide)
    elif spec_type == "linear":
        threoretical_spectrum = generate_linear_spectrum(peptide)
    # get number of occuerence of each integer using Counter Object
    threoretical_counter = Counter(threoretical_spectrum)
    experiment_counter = Counter(spectrum)
    uniq_spectrum = set(spectrum)
    return sum(min(threoretical_counter[s], experiment_counter[s])
               for s in uniq_spectrum)


def trim_leaderbord(leaderbord, spectrum, N):
    """Input: A collection of peptides Leaderboard, a collection of
              integers Spectrum, and an integer N.
       Output: The N highest-scoring linear peptides on Leaderboard
               with respect to Spectrum."""
    # list of tuples [(peptide,score),..)
    peptide_score = [(peptide, compute_spectrum_score(peptide,
                                                      spectrum,
                                                      'linear'))
                     for peptide in leaderbord]
    peptide_score.sort(key=lambda x: x[1], reverse=True)
    for i in range(N, len(leaderbord)):
        if peptide_score[i][1] < peptide_score[N-1][1]:
            return {ps[0] for ps in peptide_score[:i]}
    return {ps[0] for ps in peptide_score}


def leaderboder_cyclic_sequence(spectrum, N):
    """"Input: An integer N and a collection of integers Spectrum.
        Output: LeaderPeptide """
    leader_peptide = ""
    leaderbord = {""}
    max_mass = max(spectrum)
    while len(leaderbord) > 0:
        leaderbord = expand_peptide(leaderbord)
        copy = leaderbord.copy()
        for peptide in copy:
            mass = peptide_to_integer(peptide)
            if mass == max_mass:
                score = compute_spectrum_score(peptide, spectrum, "linear")
                leader_score = compute_spectrum_score(leader_peptide,
                                                      spectrum,
                                                      "linear")
                if score > leader_score:
                    leader_peptide = peptide
            elif mass > max_mass:
                leaderbord.remove(peptide)
        leaderbord = trim_leaderbord(leaderbord, spectrum, N)
    return leader_peptide


def spectrum_convolution(spectrum):
    """Compute the convolution of a spectrum.
       Input: A collection of integers Spectrum.
       Output: The list of elements in the convolution of Spectrum.
               If an element has multiplicity k, it should appear exactly
               k times; you may return the elements in any order."""
    spectrum.sort()
    l = len(spectrum)
    convolution = [spectrum[j]-spectrum[i] for i in range(l)
                                           for j in range(i+1,l)]
    convolution.sort()
    return convolution

def top_m_convolution(m, convolution):
    conv_counter = Counter(convolution).items()
    conv_counter.sort(key=lambda x:x[1], reverse = True)
    top_k = 0
    top_convs = []
    for i in range(len(conv_counter)):
        conv, count = conv_counter[i]
        print conv, count
        if conv < 200 and conv > 57:
            top_convs.append(conv)
            top_k += 1
            if top_k > m:
                break
    return top_convs


def expand_peptide_realword(peptides, convolution):
    """expand a integer in the convolution"""
    return {peptide.append(i) for peptide in peptides for i in convolution}


def leaderbord_by_convolution(m, n, spectrum):
    """Input: An integer M, an integer N,
              and a collection of (possibly repeated) integers Spectrum.
       Output: A cyclic peptide LeaderPeptide with amino acids taken only
               from the top M elements(and ties) of the convolution of Spectrum
               that fall between 57 and 200, and where the size of Leaderboard
               is restricted to the top N (and ties)."""
    convolution = spectrum_convolution(spectrum)
    top_conv = top_m_convolution(m, convolution)
    leader_peptide = []
    leaderbord = set([])
    max_mass = max(spectrum)
    while len(leaderbord) > 0:
        leaderbord = expand_peptide_realword(leaderbord, top_conv)
        copy = leaderbord.copy()
        for peptide in copy:
            mass = peptide_to_integer(peptide)
            if mass == max_mass:
                score = compute_spectrum_score(peptide, spectrum, "linear")
                leader_score = compute_spectrum_score(leader_peptide,
                                                      spectrum,
                                                      "linear")
                if score > leader_score:
                    leader_peptide = peptide
            elif mass > max_mass:
                leaderbord.remove(peptide)
        leaderbord = trim_leaderbord(leaderbord, spectrum, n)
    return leader_peptide




