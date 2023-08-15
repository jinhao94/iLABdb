#!/bin/sh
## $1 the results of bakta tsv
## $2 output file
 
# egrep -w "(rrs|rrf|rrl)" $1 | grep -w -v truncated | perl -a -F"\t" -lne 'print "@F[5]\t@F[0]\t@F[2]\t@F[3]\t@F[4]\t@F[7]" ' > $2

egrep -w "(rrs|rrf|rrl)" $1 | egrep -e "(partial|truncated)" -v | perl -a -F"\t" -lne 'print "@F[0]\t@F[7]\t@F[2]\t@F[3]\t@F[5]" ' > $2