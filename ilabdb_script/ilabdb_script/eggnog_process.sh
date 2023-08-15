#!/bin/bash
## $1 eggnog file
## $2 KO loca
## $3 prefix
## $4 ko count
## $5 PFAM loca
## $6 PFAM count


grep -v "^#" $1 | cut -f1,12 | perl -e 'open OT, ">@ARGV[0]"; print OT "Gene\tKO\n" ; while(<STDIN>){@s=split /\t/; if($_=~/ko:(K\d+)/){$o="@s[0]\t$1\n"; print OT $o; print "$o"} }' $2 | cut -f2 | sort | uniq -c | awk -F" " '{print $2"\t"$1}' | sed "1iV1\t$3" > $4

# sed '1,5d' $1 | cut -f1,21 | perl -e 'open OT, ">@ARGV[0]"; print OT "Gene\tKO\n" ; while(<STDIN>){@s=split /\t/; if($_=~/ko:(K\d+)/){$o="@s[0]\t$1\n"; print OT $o; print "$o"} }' $2 | cut -f2 | sort | uniq -c | awk -F" " '{print $2"\t"$1}' | sed "1iItem\t$3" > $4

grep -v "^#" $1 | cut -f1,21 | perl -lane 'print $_ if @F[1] ne "-"' | perl -e 'open OT, ">@ARGV[0]"; print OT "Gene\tPFAM\n" ; while(<STDIN>){@s=split /\t/; if(@s[1]=~/(.*?)\,.*/){$o="@s[0]\t$1\n"}else{$o="$_"}; print OT $o; print "$o" }' $5 | cut -f2 | sort | uniq -c | awk -F" " '{print $2"\t"$1}' | sed "1iItem\t$3" > $6
