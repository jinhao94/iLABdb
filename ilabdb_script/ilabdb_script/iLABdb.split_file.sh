mkdir $2
n=`awk 'END{print NF}' $1`; for i in `seq 2 $n`; do echo "cut -f1,$i $1 | awk '\$2!=0' > $2/`head -n 1 $1 | cut -f $i`.KO"; done | parallel -j 30 {}
