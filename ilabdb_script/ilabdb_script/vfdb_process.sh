#!/bin/sh
## $1 the results of diamond out 
## $2 output file
 
get_besthits.sh $1 | csvtk join -f"2;1" -t -T -H - /ddn/database/VFDB/VFDB_setB_pro.des | perl -a -F"\t" -lne '@F[-1]=~/\[(.*?)\s+\(.*?\)\s+-\s+(.*?)\s+\(/; print "@F[0]\t@F[1]\t$1\t$2" ' | sed "1iGene\tVFID\tVF_name\tVF_category" > $2
