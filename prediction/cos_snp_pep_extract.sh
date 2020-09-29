#!/bin/bash

if [ ! $1 ]; then
    $1='cos_fasta.txt'
fi

awk '{NF=4}1' $1 >mut_seq.txt
sort mut_seq.txt | uniq -c | sort -rn >sorted_seq.txt
awk '{if($1>2)print$0}' sorted_seq.txt >gt3seq.txt
cut -c 9- gt3seq.txt >result.txt

rm gt3seq.txt sorted_seq.txt mut_seq.txt

awk '
    {
        if($2>9 && length($4)-$2>10){ print substr($4, $2-9, 21), 11, $1, $3 }
        else if(length($4)-$2<=10){ print substr($4, $2-9, length($4)-$2+10), 11, $1, $3 }
        else{ print substr($4, 1, $2+11), $2+1, $1, $3 }
    }
' result.txt >mut_pep.txt

awk '
    { 
        for(i=8;i<12;i++){
            for(pos=$2-i+1;pos<=$2;pos++){
                if(pos>0 && pos<=length($1)-i+1) print substr($1, pos, i), $2-pos+1, $3, $4
            }
        } 
    }
' mut_pep.txt >cos_pep.txt

rm result.txt mut_pep.txt
