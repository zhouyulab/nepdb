import csv
import os
import sys
from itertools import islice


OUT_DIR = sys.argv[1]


def checkLineCount():
    res_dir_list = [ os.path.join(os.getcwd(), OUT_DIR, x) for x in os.listdir(os.path.join(os.getcwd(), OUT_DIR)) ]

    for res_dir in res_dir_list:
        tsv_file_list = [ os.path.join(res_dir, x) for x in os.listdir(res_dir) if '.tsv' in x ]

        line_count = 0
        for file_path in tsv_file_list:
            tsv_in = open(file_path, 'r')

            count = 0
            tsv_reader = csv.reader(tsv_in, delimiter='\t')
            for line in tsv_reader:
                count += 1

            if line_count:
                assert line_count == count
            else:
                line_count = count

            tsv_in.close()


def checkHlaFile():
    res_dir_list = [ os.path.join(os.getcwd(), OUT_DIR, x) for x in os.listdir(os.path.join(os.getcwd(), OUT_DIR)) ]

    for res_dir in res_dir_list:
        hla_tmp_list = [
            'A0101', 'A0201', 'A0202', 'A0203', 'A0204', 'A0205', 'A0206', 'A0207', 'A0211', 'A0301', 'A1101', 'A1102', 'A2301', 
            'A2402', 'A2407', 'A2501', 'A2601', 'A2902', 'A3001', 'A3002', 'A3101', 'A3201', 'A3301', 'A3303', 'A3401', 'A3402', 
            'A3601', 'A6601', 'A6801', 'A6802', 'A7401', 'B0702', 'B0704', 'B0801', 'B1301', 'B1302', 'B1402', 'B1501', 'B1502', 
            'B1503', 'B1510', 'B1517', 'B1801', 'B2705', 'B3501', 'B3503', 'B3507', 'B3701', 'B3801', 'B3802', 'B4001', 'B4002',
            'B4006', 'B4201', 'B4402', 'B4403', 'B4501', 'B4601', 'B4901', 'B5001', 'B5101', 'B5201', 'B5301', 'B5401', 'B5501', 
            'B5502', 'B5601', 'B5701', 'B5703', 'B5801', 'B5802', 'C0102', 'C0202', 'C0302', 'C0303', 'C0304', 'C0401', 'C0403', 
            'C0501', 'C0602', 'C0701', 'C0702', 'C0704', 'C0801', 'C0802', 'C1202', 'C1203', 'C1402', 'C1403', 'C1502', 'C1601', 
            'C1701', 'G0101', 'G0103', 'G0104'
        ]
        for tsv_file in os.listdir(res_dir):
            file_path = os.path.join(res_dir, tsv_file)

            with open(file_path, 'r') as tsv_in:
                tsv_reader = csv.reader(tsv_in, delimiter='\t')
               
                for line in islice(tsv_reader, 0, 1):
                    hla = line[2][6:]
                    try:
                        hla_tmp_list.remove(hla)
                    except ValueError:
                        print(f"{res_dir}: {hla} not found")

        if len(hla_tmp_list) > 0:
            print(f"{res_dir}: {hla_tmp_list} not found")


if __name__ == "__main__":
    checkLineCount()
    checkHlaFile()