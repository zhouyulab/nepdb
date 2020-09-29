"""
Unify cancer name
"""

def unifyCancerName(cancer_type_file, original_input, output):
    cancer_dict = {}
    for line in cancer_type_file:
        origin_name, unified_name = line.strip("\n").split(",")[0:2]
        cancer_dict[origin_name] = unified_name

    tmp_data_list = []
    for line in original_input:
        read_list = line.strip("\n").split(",")

        if cancer_dict.get(read_list[2]):
            read_list[2] = cancer_dict[read_list[2]]
        else:
            print(read_list[2])
            assert read_list[2] in cancer_dict.values()

        tmp_data_list.append(read_list)

    for data in tmp_data_list:
        output.write(",".join(map(str, data)) + "\n")


def main():
    CANCER_TYPE_FILE_PATH = "../data/Cancertype_correction.csv"
    INPUT_PATH = "../test/new_neg_join_se_NA_anti.csv"
    OUTPUT_PATH = "../test/new_neg_join_se_NA_anti_cancer.csv"
    WITH_HEADER = True

    with open(CANCER_TYPE_FILE_PATH) as cancer_type_file, open(INPUT_PATH) as in_file, open(OUTPUT_PATH, 'w') as out_file:
        if WITH_HEADER:
            out_file.write(in_file.readline())
        unifyCancerName(cancer_type_file, in_file, out_file)


if __name__ == "__main__":
    main()
