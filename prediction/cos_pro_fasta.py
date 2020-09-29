"""
Based on the location information and WILD, and the transcript ID to find the corresponding protein sequence
"""
from Bio import SeqIO

COS_SNP_FILE = "../data/comic_snp.txt"
OUTPUT_FILE = "../data/cos_fasta.txt"
FASTA_FILE = "../data/Homo_sapiens.GRCh38.pep.all.fa" # human reference protein sequence

fasta_file = SeqIO.parse(FASTA_FILE, "fasta")    

name_fasta = {}
for line in fasta_file:
    name = line.description
    seq = line.seq
    name = name.split(" ")
    enst = name[4].split(":")[1]
    name_fasta[enst] = seq

    
with open(COS_SNP_FILE,"r") as cos_snp, open(OUTPUT_FILE,"w") as output:
    for line1 in cos_snp:
        line = line1.strip("\n").split("\t")
        cos_enst = line[1]
        for key_ref in name_fasta:
            if key_ref == cos_enst:
                aa_pos = line[2].split(".")[1]
                wild_aa = aa_pos[0]
                if  "?" in aa_pos or "X" in aa_pos:    
                    break
                pos_mut = aa_pos[1:].split("^")
                position = pos_mut[0][:-1]
                position = int(position)-1
                sequence = name_fasta[key_ref]
                
                if position >= len(sequence): 
                    break
                if sequence[position] == wild_aa:  
                    
                    for i in range(len(pos_mut)):
                        if i == 0:
                            mut_aa = pos_mut[i][-1]
                        else:
                            mut_aa = pos_mut[i]
                        output.write(wild_aa+"\t"+str(position)+"\t"+mut_aa+"\t"+str(sequence)+"\t"+line1)
                        break
