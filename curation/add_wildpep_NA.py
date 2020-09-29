import sys

def addWildPepNA(nep_file, output):
    for line in nep_file:
        read_list = line.strip().split(",")

        pos = int(read_list[8]) if read_list[8] else None
        wt_pep, wt_aa, mut_pep, mut_aa = read_list[9:13]
        antigen_len = len(mut_pep)
        seq = read_list[45]

        index = -1
        if pos and wt_aa == seq[pos-1]:
            mut_protein = seq[0:pos-1] + mut_aa + seq[pos:]
            index = mut_protein.find(mut_pep)
        else:
            half_pos = int(antigen_len/2)
            if mut_pep[0:half_pos] in seq:
                index = seq.find(mut_pep[0:half_pos])
            elif mut_pep[half_pos:] in seq:
                index = seq.find(mut_pep[half_pos:]) + half_pos + 1

        tmp_data = []
        read_list[13] = str(antigen_len)
        read_list[9] = "NA" if index == -1 else seq[index:index+antigen_len]
        for x in read_list:
            tmp_data.append(x if x else "NA")

        output.write(",".join(tmp_data) + "\n")


def main():
    NEP_FILE_PATH = "../test/new_neg_join_se.csv"
    OUTPUT_PATH = "../test/new_neg_join_se_NA_anti.csv"
    WITH_HEADER = True

    if sys.argv[1:3]:
        NEP_FILE_PATH, OUTPUT_PATH = sys.argv[1:3]

    with open(OUTPUT_PATH, "w") as output, open(NEP_FILE_PATH) as nep_file:
        if WITH_HEADER:
            output.write(nep_file.readline())
        addWildPepNA(nep_file, output)


if __name__ == "__main__":
    main()
