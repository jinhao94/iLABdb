less $1 | grep -v '^#' | perl -lane '@F[-1]=~/ID=\d+_(\d+);/; $gene=@F[0]."_".$1; print "$gene\t$_" '
