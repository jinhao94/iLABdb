less -S $1 | perl -lane '@F[0]=~/(.*).fa/; $o1=$1; @F[1]=~/.*\/(.*?).fa/; $o2=$1; $o3=@F[3]/@F[4]; print "$o1\t$o2\t@F[2]\t$o3" ' | awk -F"\t" '$4>=0.3' | sed -e "1iInput Genome\tiLABdb ID\tAverage Nucleotide Identity\tCoverage" > $2
