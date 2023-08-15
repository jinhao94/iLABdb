#!/bin/sh
vfdb_res=$1
gene_loca=$2
vfdb_pos=$3

cut -f1 $vfdb_res | sed '1d' | csvtk join -t -T -H - $gene_loca | perl -lane 'print "@F[1]\t@F[4]\t@F[5]\t@F[0]"' > $vfdb_pos
