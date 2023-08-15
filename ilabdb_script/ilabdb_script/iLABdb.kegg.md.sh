#!/bin/sh
input_ko=$1
out_dir=$2
out_file=$3

java -jar /ddnstor/imau_sunzhihong/mnt1/software/omixer/omixer-rpm-1.1.jar -d /ddnstor/imau_sunzhihong/mnt1/software/omixer/new_pathway.f -c 0.66 -i $1 -o $2 -t 1

csvtk join -t -T -H ${2}/*.modules /ddnstor/imau_sunzhihong/mnt1/software/omixer/pathway.mapping | sed '1iModule_ID\tCopy number\tCompleteness\tPathway ID\t' > $3
