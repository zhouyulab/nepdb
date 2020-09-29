"""
Search for the corresponding protein sequence based on the gene name information, location information and peptide information,
 and remove the corresponding protein sequence if the location information is wrong.If the gene name is incorrect, 
 blast it to the correct gene in uniport or delete the whole message
"""

from itertools import islice

REFERENCE_FILE_PATH = '../test/sequence_id3'
INPUT_FILE_PATH = '../test/new_neg.csv'
OUPUT_FILE_PATH = './new_neg_join_se.csv'
NOT_MATCHED_FILE_PATH = './not_matched.csv'

# load data from reference file. saved as: { gene symbol: [sequence1, sequence2, ...] }
gene_record = {}

def printToOutput(output_file, line, gene_symbol, sequence):
    line[3] = gene_symbol
    line[45] = sequence
    output_file.write(','.join(line) + '\n')


with open(REFERENCE_FILE_PATH) as ref_file:
    for ref_record in ref_file:
        data_list = ref_record.strip("\n").split(" ")
        gene_record.setdefault(data_list[0], []).append(data_list[2])

with open(INPUT_FILE_PATH) as input_file, open(OUPUT_FILE_PATH, 'w') as output_file, open(NOT_MATCHED_FILE_PATH, 'w') as not_match:
    for line in islice(input_file, 1, None):
        read_list = line.strip().split(',')
        gene_symbol = read_list[4]
        position = int(read_list[8]) if read_list[8] else None
        motif = read_list[9]
        wild_AA = read_list[10]

        if gene_symbol in gene_record:
            for sequence in gene_record[gene_symbol]:
                if position:
                    if position <= len(sequence) and sequence[position - 1] == wild_AA:
                        index = sequence.find(motif, position-len(motif), position+len(motif)-1)
                        if index != -1:
                            printToOutput(output_file, read_list, gene_symbol, sequence)
                else:
                    index = sequence.find(motif)
                    if index != -1:
                        printToOutput(output_file, read_list, gene_symbol, sequence)
        else:
            printToOutput(not_match, read_list, gene_symbol, sequence)
    

