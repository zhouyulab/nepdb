#!/bin/bash

filename=$1
lines=$2

file=${filename%.*}
ext=${filename#*.}

awk -v count=$lines -v file=${file} -v ext=${ext} 'BEGIN {i=1} {
    if (NR == i*count-count+1) { print "pep" > "input/"file"_"i"."ext; }
    print $0 > "input/"file"_"i"."ext;
    if (NR >= i*count) { close("input/"file"_"i"."ext); i++; }
}' $filename
