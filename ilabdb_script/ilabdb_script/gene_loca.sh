#!/bin/sh
## $1 the results of bakta tsv
## $2 output file

# grep -v "^#" $1 | awk -F"\t" '$2!="crispr" && $2!="ncRNA-region"'  | perl -a -F"\t" -lne 'print "@F[5]\t@F[0]\tBakta\t@F[1]\t@F[2]\t@F[3]\t@F[4]\t@F[7]" ' > $2

sed 's/.giLABdb//g' $1 | grep -v "^#" | perl -a -F"\t" -lne 'next if length(@F[5]) == 0; print "@F[5]\t@F[0]\tBakta\tCDS\t@F[2]\t@F[3]\t200\t@F[4]\t0\t@F[7]" ' > $2