#!/bin/bash

dir=$1
seq_count=0

for element in `ls $dir`
do
    file=$dir/$element'/A0101.tsv'

    cat $file | awk '{if (NR>1) {print $1;}}' >> pred_pep.txt
    line_count=`cat $file|wc -l`
    seq_count=`expr ${seq_count} + ${line_count} - 1`
done

sort cos_pep.txt pred_pep.txt pred_pep.txt | uniq -u > not_pred_pep.txt
echo $seq_count" seqeunces has been predicted."
