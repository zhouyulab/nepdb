"""Based on the transcript ID information provided by your data, look for the corresponding protein sequence"""

import re
from Bio import SeqIO

ENST_FASTA_PATH = "../data/ENS_ID.fa"
UCSC_TRANS_FASTA_FILE = "../data/UCSCtran_ID"
NCBI_REFSEQ_FILE = "../data/mRNA_ID"
OUTPUT_FILE = "./transcript_seq.csv"


ruleNCBI = re.compile("NM_\d+")
ruleEN = re.compile("ENST\d+")
ruleUC = re.compile("(uc\w+)\.\d+")

UCSC = []
ENSM = []
NCBI = []
NULL = []
TABLE_HEADER_STR = ""

with open ("../test/new_neg.csv") as in_file:
    for readline in in_file:
        if readline.startswith("response"):
            TABLE_HEADER_STR = readline
        line = readline.strip("\n").split(",")
        transname = line[7]
        if re.findall(ruleEN, transname):
            ENSM.append(line)
        elif re.findall(ruleNCBI, transname):
            NCBI.append(line)
        elif re.findall(ruleUC, transname):
            UCSC.append(line)
        else:
            NULL.append(line)

allmatch = []

'''Extract the sequence in ENST ID'''
fasta_content1 = SeqIO.parse(ENST_FASTA_PATH, "fasta")
for seq_record1 in fasta_content1:
    a = seq_record1.seq
    gid = re.findall(ruleEN, seq_record1.description)[0]
    for enline in ENSM:
        if enline[7] == gid:
            enline[45] = a
            allmatch.append(",".join(map(str, enline))+ "\n")

'''Extract the sequence from UCSC ID'''
fasta_content2 = SeqIO.parse(UCSC_TRANS_FASTA_FILE, "fasta")
for seq_record2 in fasta_content2:
    a = seq_record2.seq
    UCSC_ID = seq_record2.id
    for ucline in UCSC:
        if ucline[7] == UCSC_ID:
            ucline[45] = a
            allmatch.append(",".join(map(str, ucline)) + "\n")

'''Extract the sequence from NCBI ID'''
with open(NCBI_REFSEQ_FILE) as file2, open(OUTPUT_FILE, "w") as output:
    match = []
    for line2 in file2:
        line2 = line2.strip("\n").split(" ")
        gene2 = line2[0]
        geneid = line2[1]
        geneid2 = geneid.split(".")[0]
        protein_id = line2[2]
        sequence = line2[3]
        size = len(sequence)
        for ncline in NCBI:
            if ncline[7] == geneid2:
                ncline[45] = sequence
                allmatch.append(",".join(map(str, ncline)) + "\n")

    output.write(TABLE_HEADER_STR)
    for merge in allmatch:
        output.write(merge)