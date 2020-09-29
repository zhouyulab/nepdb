"""
According to the mutation frequency of amino acid mutation  greater than or equal to 3, corresponding mutation information was obtained, 
and then short peptides 8,9,10,11 were intercepted according to the information.
"""
count = {}
COS_SEQ = "../data/cos_sequence.txt"
COS_PEP = "../data/cos_pep.txt"

with open(COS_SEQ) as f :
    for line in f :
        line = line.strip("\n").split("\t")
        gene_pos = line[0]+"\t"+line[1] +"\t"+line[2]+"\t"+line[3]
        count.setdefault(gene_pos, 0)
        count[gene_pos] = count[gene_pos] + 1

pep_file = open(COS_PEP,"w")

enst_position = []
rep_pep = []
for key,value in count.items():
    if value >=3 :
        enst_position.append(key)     
        wild_pos_mut_seq = key.strip("\n").split("\t")
        mut = wild_pos_mut_seq[2]
        wild = wild_pos_mut_seq[0]
        positi = int(wild_pos_mut_seq[1])
        sequence  = wild_pos_mut_seq[3]
        x = list(sequence)
        x[positi] = mut
        sequence = ''.join(x)
        
        seq_length = len(sequence)
        for pep_len in [8,9,10,11]:
            for i in range(positi-pep_len+1,positi+1):
                if pep_len <= seq_length-i and i>=0 and sequence[i:i+pep_len] not in rep_pep :
                    rep_pep.append(sequence[i:i+pep_len])
                    pep_file.write(sequence[i:i+pep_len]+"\n")
pep_file.close()
