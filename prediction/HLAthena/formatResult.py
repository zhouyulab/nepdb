import csv
import os
import sys

OUT_DIR = sys.argv[1] if sys.argv[1] else 'format'
res_dir_list = [ os.path.join(os.getcwd(), OUT_DIR, x) for x in os.listdir(os.path.join(os.getcwd(), OUT_DIR)) ]
# assert len(res_dir_list) == 24

for res_dir in res_dir_list:
    tsv_file_list = [ os.path.join(res_dir, x) for x in os.listdir(res_dir) if '.tsv' in x ]
    assert len(tsv_file_list) == 95

    line_count = 0
    for file_path in tsv_file_list:
        tsv_in = open(file_path, 'r')

        count = 0
        tsv_reader = csv.reader(tsv_in, delimiter='\t')
        for index, line in enumerate(tsv_reader):
            if index == 0:
                hla_type = line[2][6:]
            else:
                count += 1

        if line_count:
            assert line_count == count
        else:
            line_count = count

        tsv_in.close()

        os.rename(file_path, os.path.join(res_dir, f'{hla_type}.tsv'))   