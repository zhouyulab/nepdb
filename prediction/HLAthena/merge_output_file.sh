#!/bin/bash

dir=$1

for file in `ls $1'/cos_pep_1'`
do
    cat format/**/$file > 'temp/'$file
done


for merged_file in `ls 'temp'`
do
    hla=${merged_file%.*}
    awk -v hla=$hla 'BEGIN{ FS="\t"; OFS="\t"; } {
        print hla,$1,$4,$5
    }' 'temp/'$merged_file >> all.tsv
done

rm temp/*