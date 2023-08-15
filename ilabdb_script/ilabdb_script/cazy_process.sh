#!/bin/sh
## $1 the results of diamond out 
## $2 output file
 
get_besthits.sh $1 | cut -f1,2 | perl -lane '@s=split /\|/, @F[1]; if(@s[1]=~/(.*?)_/){$o=$1}else{$o=@s[1]}; if($o=~/(\D+)/){$c=$1}; print "@F[0]\t$o\t$c"' | sed "1iGene\tCAZY_category\tCAZY_family" > $2