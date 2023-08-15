#!/bin/sh

less $1 | perl -a -F"\t" -lne 'BEGIN{print "iLABdb_ID\tTotal regions\tRegion ID\tContig region ID\tFunction description\tFunction Type\tStart\tEnd\tLength"; }; if($_=~/^iLABdb_ID/){print $_; next}elsif(@F[3]=~/^c0(\d+)/){$t=$1; $t=~s/^0+//; @F[3]="@F[0]_${t}"; $o=(join "\t", @F)}else{$o=$_}; print $o ' >  $2