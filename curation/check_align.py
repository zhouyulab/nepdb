#!/usr/bin/env python

"""
Validate and correct cancer neo-antigen information
"""
import os
import sys
from Bio import pairwise2

def align_wt_mut_peptides(wt_peptide, mut_peptide):
    """
    Align two peptides with 1 or more mismatches
    with custom scoring (match, mismatch, gap-open, gap-extend)
    """
    return pairwise2.align.globalms(
        wt_peptide, mut_peptide, 5, -2, -6, -2,
        penalize_extend_when_opening=True, penalize_end_gaps=False)


def find_mismatch_pair(align1, align2):
    """
    Return a list of mismatched pair aa (a, b)
    """
    mmli = []
    for a, b in zip(align1, align2):
        if a != b and a != "-" and b != "-":
            mmli.append((a, b))
    return mmli

def format_align(align1, align2, score, begin, end):
    """
    Formatting alignment from pairwise2
    """
    assert begin == 0 and len(align1) == len(align2) and len(align1) == end
    s = []
    s.append(align1)
    aln = []
    aln.append(" " * begin)
    for a, b in zip(align1[begin:end], align2[begin:end]):
        if a == b:
            aln.append("|")  # match
        elif a == "-" or b == "-":
            aln.append(" ")  # gap
        else:
            aln.append(".")  # mismatch
    s.append("".join(aln))
    s.append(align2)
    s.append("  Score=%g" % score)
    return s


def substring_indexes(substring, string):
    """ 
    Generate indices of where substring begins in string
    >>> list(substring_indexes('me', "The cat says meow, meow"))
    [13, 19]
    """
    last_found = -1  # Begin at -1 so the next position to search from is 0
    while True:
        # Find next index of substring, by starting after its last known position
        last_found = string.find(substring, last_found + 1)
        if last_found == -1:  
            break  # All occurrences have been found
        yield last_found

if len(sys.argv) < 3:
    print("Usage: program infile outfile\n")
    sys.exit(1)

f_necid, outfile = sys.argv[1:3] #"20180626dataR1.csv"
assert os.path.exists(f_necid)
foh = open(outfile, "w")
foh_error = open(f_necid+".ERROR.csv", "w")

lines = [line.rstrip().split(",") for line in open(f_necid)]
foh.write(",".join(lines[0] )+ "\n")
foh_error.write(",".join(lines[0] + ["ERROR"])+"\n")

for i in range(len(lines)):
    b = lines[i]
    if b[45].startswith("protein_sequence"):
        continue

    skip = False
    msgs = []
    def log(*args):
        global msgs
        msg = " ".join(map(str, args))
        msgs.append(msg)
        print(msg)

    mut_aa_pos, wt_peptide, wt_aa, mut_peptide, mut_aa, antigen_len = b[8:14]
    pro = b[45]

    ## Skip record without protein sequence
    if len(pro) <= 0:
        log(i, "No protein sequence")
        skip = True
        foh_error.write(",".join(b + ["; ".join(msgs)])+"\n")
        continue

    ## Find correct wt_peptide interval in protein sequence
    ## Reset mut_aa_pos if not in wt_peptide interval 
    numpep = pro.count(wt_peptide) 
    starts = list(substring_indexes(wt_peptide, pro))
    wt_pep_start = 'NA' # global start position of wt_peptide in protein sequence
    mut_pos_in_pep = 'NA' # local start postion of mutation in wt_peptide
    mutpos = int(mut_aa_pos)-1 if mut_aa_pos != 'NA' else 'NA'
    if numpep == 0:
        log(i, "No wt_peptide found in protein")
        skip = True
        foh_error.write(",".join(b + ["; ".join(msgs)])+"\n")
        continue
    elif numpep == 1:
        wt_pep_start = starts[0]
        if mut_aa_pos != 'NA':
            if not (wt_pep_start <= mutpos < wt_pep_start+len(wt_peptide)): 
                log(i, "mut_pos not in wt_peptide interval")
                mut_aa_pos = 'NA'
    elif numpep > 1:
        if mut_aa_pos != 'NA':
            for k in range(numpep):
                start = starts[k]
                end = start + len(wt_peptide)
                if mutpos >= start and mutpos < end:
                    wt_pep_start = start # found wt_peptide interval covering mut_aa_pos
                    break

            if wt_pep_start == 'NA':
                log(i, "No wt_peptide interval covering mut_aa_pos (%s): [%s]" % (
                    mut_aa_pos, " ".join(map(str, starts))))
                mut_aa_pos = 'NA' # reset as not available
                
    ## Check if AA at mut_aa_pos identical to wt_aa
    if mut_aa_pos != 'NA' and wt_pep_start != 'NA': 
        if pro[mutpos:(mutpos+len(wt_aa))] != wt_aa:
            log(i, "WT AA at mut_pos != wt_aa", pro[mutpos], wt_aa)
            mut_aa_pos = 'NA'

    ## Try determine mut_aa_pos if wt_aa occurs only once in wt_peptide
    if mut_aa_pos == 'NA':
        numaa = wt_peptide.count(wt_aa)
        if numaa == 1:
            mut_pos_in_pep = wt_peptide.index(wt_aa)
            if wt_pep_start != 'NA':
                mut_aa_pos = wt_pep_start + mut_pos_in_pep + 1
                mutpos = mut_aa_pos - 1
    else:
        mut_pos_in_pep = int(mut_aa_pos) - 1 - wt_pep_start
        
    ## Generate mut_peptide if not given
    if mut_peptide == 'NA':
        if mut_aa_pos != 'NA' and mut_aa != 'NA':
            mut_peptide = list(wt_peptide)
            mut_peptide[mut_pos_in_pep] = mut_aa
            mut_peptide = ''.join(mut_peptide)
            log(i, "mut_peptide generated from wt_aa to mut_aa") 
        
    ## Validate the (wt_aa, mut_aa) occurs in the list of mismatches between wt and mut peptides
    num_mm = 'NA'
    pep2aln = ''
    if wt_peptide != 'NA' and mut_peptide != 'NA':
        alignments = align_wt_mut_peptides(wt_peptide, mut_peptide)
        if len(alignments) >= 2:
            log(i, "wt_peptide and mut_peptide have >=2 best alignments")
        alignment = alignments[0]
        alns = format_align(*alignment) 
        num_mm = alns[1].count(".")
        pep2aln = "\t".join(alns[:3])
        num_gap = alns[1].strip(" ").count(" ")
        print(i, num_mm, num_gap)
        print('\n'.join(alns))
        align1, align2 = alignment[:2]
        mmli = find_mismatch_pair(align1, align2)
        mmin = [(wta, mutb) in mmli for wta, mutb in zip(wt_aa, mut_aa)]
        if not all(mmin):
            errmsg = "expected (%s=>%s) not in mismatched pairs" % (wt_aa, mut_aa)
            log(i, errmsg)
            skip = True

    elif mut_peptide == 'NA':
        log(i, 'mut_peptide not available')
        skip = True
    elif wt_peptide == 'NA':
        log(i, 'wt_peptide not available')
        skip = True

    foh_error.write(",".join(b + ["; ".join(msgs)])+"\n")
    if skip:
        continue

    ## Update validated record
    if mut_aa_pos == 'NA':
        b[8] = mut_aa_pos
    if mut_peptide != 'NA':
        b[14] = mut_peptide
    if wt_pep_start != 'NA':
        wt_pep_start= wt_pep_start+1
    if mut_pos_in_pep != 'NA':
        mut_pos_in_pep =mut_pos_in_pep+1
    a=b[0:46]+[numpep, wt_pep_start, mut_pos_in_pep, num_mm, num_gap, pep2aln, "; ".join(msgs)]+b[52:]
    # b += [numpep, wt_pep_start, mut_pos_in_pep, num_mm, num_gap, pep2aln, "; ".join(msgs)]
    foh.write(",".join(map(str, a))+"\n")
    print("\n\n")
    
foh_error.close()
foh.close()
