#!/bin/sh
if [ $# == 0 ];then
    echo "Useage: Bin_gutsmash.sh gut_smash.result/index.html > gut_smash.result.summary"
    exit
fi

egrep "(classes|Location|Region |\<title\>)" $1 | perl -e '@NT_list=(); @C_list=(); @LL_list=(); while(<STDIN>){chomp; if($_=~/<title>(.*?)\s-\s(\d+ region\(s\))/ ){$title=$1; $num_region=$2; next}; if($_=~/class=\"heading\">\s(.*?)\s-\s(Region\s\d+)\s-\s(.*?)\s</){$name=$1."_".$2; $type=$3; push @NT_list, $name."\t".$type; next}; if($_=~/classes" target="_blank">(.*?)</){$class=$1; push @C_list, $class; next}; if($_=~/Location:\s(.*?)\s-(.*?)\snt.*\(total:\s(.*)\snt/){$loc=$1."\t".$2."\t".$3; push @LL_list, $loc; next} }; $total_region=$#NT_list+1; for($i=0; $i<$total_region; $i+=1){$o=@NT_list[$i]."\t".@C_list[$i]."\t".@LL_list[$i]; $ct=$i+1; print "$title\t$num_region\t$ct\t$o\n" }' | perl -a -F"\t" -lne 'BEGIN{print "iLABdb_ID\tTotal regions\tRegion ID\tContig region ID\tFunction description\tFunction Type\tStart\tEnd\tLength"; }; if($_=~/^iLABdb_ID/){print $_; next}elsif(@F[3]=~/^c0(\d+)/){$t=$1; $t=~s/^0+//; @F[3]="@F[0]_${t}"; $o=(join "\t", @F)}else{$o=$_}; print $o '
