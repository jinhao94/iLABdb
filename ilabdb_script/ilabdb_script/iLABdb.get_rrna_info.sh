less $1 | grep "S ribosomal RNA" | perl -a -F"\t" -lne '@F[-1]=~/Name=(.*?);/; print "@F[0]\t$1\t@F[3]\t@F[4]\t@F[-1]" ' | egrep -v "(partial)"  
