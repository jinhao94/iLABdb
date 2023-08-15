#!/bin/sh
input_gff=$1
chromsize=$2
grep 'Sequence Data' $input_gff | sed -e 's/=/\t/g' -e 's/;/\t/g' -e 's/"/\t/g' | awk 'BEGIN{OFS=FS="\t"}{print $7,$4}' > $chromsize
